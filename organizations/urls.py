from django.urls import path, include
from rest_framework.routers import DefaultRouter

from organizations.views import dicts, organizations, employees, \
    departments, offers, members

router = DefaultRouter()

router.register(r'dicts/positions', dicts.PositionView, 'positions')
router.register(r'search', organizations.OrganizationSearchView, 'organizations-search')
router.register(r'(?P<pk>\d+)/employees', employees.EmployeeView, 'employees')
router.register(r'offers', offers.OfferUserView, 'user-offers')
router.register(r'(?P<pk>\d+)/offers', offers.OfferOrganizationView, 'org-offers')
router.register(r'departments/(?P<pk>\d+)/members', members.MemberView, 'members')
router.register(r'departments', departments.DepartmentView, 'departments')
router.register(r'', organizations.OrganizationView, 'organizations')


urlpatterns = [
    path('organizations/', include(router.urls)),
]
