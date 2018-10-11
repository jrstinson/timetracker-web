import factory
import pytest


class EmployeeFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating test employees.
    """
    company = 'Acme Inc.'
    supervisor = 'John Smith'
    user = factory.SubFactory('conftest.UserFactory')

    class Meta:
        model = 'vms.Employee'


class TimeRecordApprovalFactory(factory.DjangoModelFactory):
    """
    Factory for generating test time record approvals.
    """
    time_record = factory.SubFactory('vms.test.conftest.TimeRecordFactory')
    user = factory.SubFactory('conftest.UserFactory')

    class Meta:
        model = 'vms.TimeRecordApproval'


class TimeRecordFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating test time records.
    """
    employee = factory.SubFactory('vms.test.conftest.EmployeeFactory')

    class Meta:
        model = 'vms.TimeRecord'


@pytest.fixture
def employee_factory(db):
    """
    Fixture to get the factory used to create employees.
    """
    return EmployeeFactory


@pytest.fixture
def time_record_approval_factory(db):
    """
    Fixture to get the factory used to create time record approvals.
    """
    return TimeRecordApprovalFactory


@pytest.fixture
def time_record_factory(db):
    """
    Fixture to get the factory used to create time records.
    """
    return TimeRecordFactory