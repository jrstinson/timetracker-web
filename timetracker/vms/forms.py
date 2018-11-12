import logging

from django import forms
from django.utils import timezone
from django.utils.translation import ugettext as _, ugettext_lazy

from vms import models


logger = logging.getLogger(__name__)


class ClientAdminInviteAcceptForm(forms.Form):
    """
    Form to accept an invitation to become a client admin.
    """

    def __init__(self, token, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.token = token
        self.invite = None

    def clean(self):
        """
        Ensure the provided token is valid.
        """
        query = models.ClientAdminInvite.objects.filter(token=self.token)

        if not query.exists():
            raise forms.ValidationError(
                _('The provided invitation code is invalid.'),
            )

        self.invite = query.get()

    def save(self, user):
        """
        Accept the invitation with the provided token.

        Args:
            user:
                The user who is accepting the invitation.

        Returns:
            The newly created ``ClientAdmin`` instance.
        """
        return self.invite.accept(user)


class ClientCreateForm(forms.ModelForm):
    """
    Form to create a new client.

    Once the form is saved, a new client company is saved, and an email
    invitation to become an admin for the client is sent to the provided
    email address.
    """
    admin_email = forms.EmailField(
        help_text=ugettext_lazy(
            'The email address of the person who will be made an '
            'administrator of the new client.'
        ),
        label=ugettext_lazy('Admin Email Address'),
    )

    class Meta:
        fields = ('name', 'email', 'phone_number', 'admin_email', 'notes')
        model = models.Client

    def save(self, request=None, commit=True):
        """
        Create a new client and send an email to the admin.

        Args:
            request:
                The request made to trigger the form save.
            commit:
                A boolean indicating if the created model should be
                saved to the database or not.

        Returns:
            The created client instance.
        """
        admin_email = self.cleaned_data.pop('admin_email')
        client = super().save(commit)

        invite = models.ClientAdminInvite.objects.create(
            client=client,
            email=admin_email,
        )
        invite.send(request)

        return client


class ClockInForm(forms.Form):
    """
    Form to clock in the requesting user.
    """
    job = forms.ModelChoiceField(empty_label=None, queryset=None)

    def __init__(self, employee, *args, **kwargs):
        """
        Instantiate the form to clock in a specific employee.

        Args:
            employee:
                The employee that will be clocked in.
            *args:
                Positional arguments for the base form class.
            **kwargs:
                Keyword arguments for the base form class.
        """
        super().__init__(*args, **kwargs)

        self.employee = employee
        self.fields['job'].queryset = models.ClientJob.objects.filter(
            client=employee.client,
        )

    def clean(self):
        """
        Validate the form to ensure the employee is not already clocked
        in.
        """
        if not self.employee.is_active:
            raise forms.ValidationError(
                _('Inactive employees are not allowed to clock in.'),
            )

        if self.employee.is_clocked_in:
            raise forms.ValidationError(
                _('You are already clocked in.')
            )

    def save(self):
        """
        Save the form to create a new time record.
        """
        record = models.TimeRecord.objects.create(
            employee=self.employee,
            pay_rate=self.cleaned_data.get('job').pay_rate,
            **self.cleaned_data,
        )
        logger.info('Created time record %r', record)


class ClockOutForm(forms.Form):
    """
    Form to clock out an employee.
    """

    def __init__(self, employee, *args, **kwargs):
        """
        Initialize the form with an employee.

        Args:
            employee:
                The employee to clock out.
            *args:
                Positional arguments to initialize the form with.
            **kwargs:
                Keyword arguments to initialize the form with.
        """
        super().__init__(*args, **kwargs)

        self.employee = employee

    def clean(self):
        """
        Validate the form's data.

        Raises:
            forms.ValidationError:
                If the employee is not clocked in.
        """
        if not self.employee.is_clocked_in:
            raise forms.ValidationError(
                _('You must be clocked in to clock out.'),
            )

    def save(self):
        """
        Complete the employee's open time record.
        """
        record = self.employee.time_records.get(time_end=None)
        record.time_end = timezone.now()
        record.save()

        logger.info('Completed time record %r', record)


class CreateStaffAgencyForm(forms.Form):
    """
    Form to create staffing agency.
    """
    email_field = forms.EmailField(required=True)
    name_field = forms.CharField(required=True)
    notes_field = forms.CharField(required=False, widget=forms.Textarea)
    regex = r'^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-'\
        r'. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$'
    phone_number_field = forms.RegexField(regex=regex, required=False)

    def save(self, user):
        agency = models.StaffingAgency.objects.create(
            email=self.data.get('email_field'),
            name=self.data.get('name_field'),
            notes=self.data.get('notes_field'),
            phone_number=self.data.get('phone_number_field')
            )
        models.StaffingAgencyAdmin.objects.create(
            user=user,
            agency=agency
        )


class TimeRecordApprovalForm(forms.Form):
    """
    Form to approve a time record.
    """

    def __init__(self, time_record, approving_user, *args, **kwargs):
        """
        Initialize the form with the time record being approved and the
        supervisor doing the approval.

        Args:
            time_record:
                The time record being approved.
            approving_user:
                The user who is approving the time record.
            *args:
                Positional arguments for the base form class.
            **kwargs:
                Keyword arguments for the base form class.
        """
        super().__init__(*args, **kwargs)

        self.time_record = time_record
        self.approving_user = approving_user

    def save(self):
        """
        Create an approval for the time record associated with the form.

        Returns:
            The approval instance created for the time record.
        """
        return models.TimeRecordApproval.objects.create(
            time_record=self.time_record,
            user=self.approving_user,
        )
