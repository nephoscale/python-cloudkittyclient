# Copyright 2015 Objectif Libre
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from cloudkittyclient.common import base
import json

class ReportResult(base.Resource):

    key = 'report'

    def __repr__(self):
        return "<Report %s>" % self._info

class ReportSummary(base.Resource):

    key = 'summary'

    def __init(self, tenant_id=None, res_type=None, begin=None,
               end=None, rate=None):
        self.tenant_id = tenant_id
        self.res_type = res_type
        self.begin = begin
        self.end = end
        self.rate = rate

    def __repr__(self):
        return "<Summary %s" % self._info


class ReportManager(base.Manager):

    base_url = '/v1/report'
    resource_class = ReportResult
    key = "report"
    collection_key = "reports"

    def list_tenants(self):
        return self.client.get(self.base_url + "/tenants").json()

    # Modified by Muralidharan.s for applying a logic for getting 
    # Total value based on Instance
    def get_total(self, tenant_id=None, begin=None, end=None, service=None,instance_id=None):
        url = self.base_url + "/total"
        filters = list()
        if tenant_id:
            filters.append("tenant_id=%s" % tenant_id)
        if begin:
            filters.append("begin=%s" % begin.isoformat())
        if end:
            filters.append("end=%s" % end.isoformat())
        if service:
            filters.append("service=%s" % service)
        if instance_id:
            filters.append("instance_id=%s" % instance_id)
        if filters:
            url += "?%s" % ('&'.join(filters))
        return self.client.get(url).json()

    # Get invoice based on tenant-id, payment_status and invoice-id args
    # added option for getting invoice based on tenant_name
    def get_invoice(self, tenant_id=None, invoice_id=None, payment_status=None, tenant_name=None):
        url = self.base_url + "/invoice"
        filters = list()
        if tenant_id:
            filters.append("tenant_id=%s" % tenant_id)
        if tenant_name:
            filters.append("tenant_name=%s" % tenant_name)
        if invoice_id:
            filters.append("invoice_id=%s" % invoice_id)
        if payment_status:
            filters.append("payment_status=%s" % payment_status)
        if filters:
            url += "?%s" % ('&'.join(filters))
        return [self.resource_class(self, j, loaded=True)
                for j in self.client.get(url).json()]
   
 
    # List the invoices, can accept all-tenants arg
    def list_invoice(self, all_tenants=None):
        url = self.base_url + "/list_invoice"
        filters = list()
        if all_tenants:
            filters.append("all_tenants=%s" % all_tenants)
        if filters:
            url += "?%s" % ('&'.join(filters))
        return [self.resource_class(self, j, loaded=True)
                for j in self.client.get(url).json()]


    # Show the invoice details
    def show_invoice(self, invoice_id):
        url = self.base_url + "/show_invoice"
        filters = list()
        if invoice_id:
            filters.append("invoice_id=%s" % invoice_id)
        if filters:
            url += "?%s" % ('&'.join(filters))
        return [self.resource_class(self, j, loaded=True)
                for j in self.client.get(url).json()]

    # Adding the invoice details, Arguments specified in kwargs 
    def add_invoice(self, **kwargs):
        url = self.base_url + "/add_invoice"
        filters = list()

        if kwargs.get('invoice_id'):
            filters.append("invoice_id=%s" % kwargs.get('invoice_id'))
        if kwargs.get('invoice_date'):
            filters.append("invoice_date=%s" % kwargs.get('invoice_date'))
        if kwargs.get('invoice_period_from'):
            filters.append("invoice_period_from=%s" % kwargs.get('invoice_period_from'))
        if kwargs.get('invoice_period_to'):
            filters.append("invoice_period_to=%s" % kwargs.get('invoice_period_to'))
        if kwargs.get('tenant_id'):
            filters.append("tenant_id=%s" % kwargs.get('tenant_id'))
        if kwargs.get('invoice_data'):
            filters.append("invoice_data=%s" % kwargs.get('invoice_data'))
        if kwargs.get('tenant_name'):
            filters.append("tenant_name=%s" % kwargs.get('tenant_name'))
        if kwargs.get('total_cost'):
            filters.append("total_cost=%s" % kwargs.get('total_cost'))
        if kwargs.get('paid_cost'):
            filters.append("paid_cost=%s" % kwargs.get('paid_cost'))
        if kwargs.get('balance_cost'):
            filters.append("balance_cost=%s" % kwargs.get('balance_cost'))
        if kwargs.get('payment_status'):
            filters.append("payment_status=%s" % kwargs.get('payment_status'))
            print(filters)
        if filters:
            url += "?%s" % ('&'.join(filters))
        return self.client.post(url).json()

    # Updating a invoice
    def update_invoice(self, **kwargs):
        """ INVOICE UPDATE """
        url = self.base_url + "/update_invoice"
        filters = list()
        if kwargs.get('invoice_id'):
            filters.append("invoice_id=%s" % kwargs.get('invoice_id'))
        if kwargs.get('total_cost'):
            filters.append("total_cost=%s" % kwargs.get('total_cost'))
        if kwargs.get('paid_cost'):
            filters.append("paid_cost=%s" % kwargs.get('paid_cost'))
        if kwargs.get('balance_cost'):
            filters.append("balance_cost=%s" % kwargs.get('balance_cost'))
        if kwargs.get('payment_status'):
            filters.append("payment_status=%s" % kwargs.get('payment_status'))
        if filters:
            url += "?%s" % ('&'.join(filters))
        return self.client.put(url).json()

    # deleting a invoice
    def delete_invoice(self, **kwargs):
        url = self.base_url + "/delete_invoice"
        filters = list()
        if kwargs.get('invoice_id'):
            filters.append("invoice_id=%s" % kwargs.get('invoice_id'))
        if filters:
            url += "?%s" % ('&'.join(filters))
        return self.client.delete(url).json()


"""
class ReportManager(base.CrudManager):

    base_url = "/v1/report"

    def list_tenants(self):
        return self.client.get(self.base_url + "/tenants").json()

    def get_total(self, tenant_id=None, begin=None, end=None,
                  service=None, all_tenants=False):
        url = self.base_url + "/total"
        filters = list()
        if tenant_id:
            filters.append("tenant_id=%s" % tenant_id)
        if begin:
            filters.append("begin=%s" % begin.isoformat())
        if end:
            filters.append("end=%s" % end.isoformat())
        if service:
            filters.append("service=%s" % service)
        if all_tenants:
            filters.append("all_tenants=%s" % all_tenants)
        if filters:
            url += "?%s" % ('&'.join(filters))
        return self.client.get(url).json()
"""

class ReportSummaryManager(ReportManager):

    resource_class = ReportSummary
    key = 'summary'
    collection_key = "summary"

    def get_summary(self, tenant_id=None, begin=None, end=None,
                    service=None, groupby=None, all_tenants=False):
        kwargs = {}
        if tenant_id:
            kwargs['tenant_id'] = tenant_id
        if begin:
            kwargs['begin'] = begin.isoformat()
        if end:
            kwargs['end'] = end.isoformat()
        if service:
            kwargs['service'] = service
        if groupby:
            kwargs['groupby'] = groupby
        if all_tenants:
            kwargs['all_tenants'] = all_tenants
        return super(ReportManager, self).list(**kwargs)
