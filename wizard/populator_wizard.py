# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import faker
import random
import re
from odoo import api, fields, models


def fake_cnpj():
    cnpj_s_dv = [random.randint(0, 9) for _ in range(12)]
    peso = [5 - i for i in range(4)] + [9 - j for j in range(8)]
    peso = sum([cnpj_s_dv[k] * peso[k] for k in range(12)]) % 11
    resto = 0 if peso < 2 else 11 - peso
    cnpj_s_dv += [resto]
    peso = [6 - i for i in range(5)] + [9 - j for j in range(8)]
    peso = sum([cnpj_s_dv[k] * peso[k] for k in range(13)]) % 11
    resto = 0 if peso < 2 else 11 - peso
    cnpj_s_dv += [resto]
    cpf = ''.join([str(d) for d in cnpj_s_dv])
    return cpf


def fake_cpf():
    def calcula_digito(digs):
        s = 0
        qtd = len(digs)
        for i in range(qtd):
            s += n[i] * (1 + qtd - i)
        res = 11 - s % 11
        if res >= 10:
            return 0
        return res                                                                              
    n = [random.randrange(10) for i in range(9)]
    n.append(calcula_digito(n))
    n.append(calcula_digito(n))
    return "%d%d%d%d%d%d%d%d%d%d%d" % tuple(n)


class OdooPopulator(models.TransientModel):
    _name = 'odoo.populator'

    generate_company = fields.Boolean(string='Generate Companies')
    company_numbers = fields.Integer(string='Number of Companies',
                                     default=random.randint(1, 10))
    generate_fisical_partner = fields.Boolean(
        string='Generate Fisical Partners')
    fisical_partner_number = fields.Integer(
        string='Number of Fisical Partners',
        default=random.randint(1, 10))
    generate_products = fields.Boolean(string='Generate Products')
    products_number = fields.Integer(string='Number of Products',
                                     default=random.randint(1, 10))
    generate_my_company = fields.Boolean(string='Generate My Company')
    generate_employees = fields.Boolean(string='Generate Employees')
    employees_number = fields.Integer(string='Number of Employees',
                                      default=random.randint(1, 10))

    def generate_own_company(self):
        fake = faker.Faker('pt_BR')
        my_company = self.env.user.company_id
        my_company.name = fake.company()
        my_company.legal_name = fake.company()
        my_company.zip = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        my_company.street = fake.street_name()
        my_company.street2 = ' '.join(fake.words(6))
        my_company.number = str(random.randint(1, 700))
        my_company.district = fake.bairro()
        estado = self.env['res.country.state'].search(
            [('country_id', '=', 32)])
        estado = random.choice(estado)
        cidade = self.env['res.state.city'].search(
            [('state_id', '=', estado.id)])
        my_company.country_id = 32
        my_company.state_id = estado.id
        my_company.city_id = random.choice(cidade).id
        my_company.website = fake.url()
        telefone = fake.phone_number()
        telefone = re.sub('\D', '', telefone)
        my_company.phone = telefone
        my_company.email = fake.email()
        my_company.cnpj_cpf = fake_cnpj()

    def generate_user(self):
        fake = faker.Faker('pt_BR')
        user = self.env['res.users']
        user_dict = {
            'name': fake.name(), 'login': fake.email(),
            'phone': fake.phone_number(),
        }
        user.create(user_dict)

    def generate_client(self, person=True):
        fake = faker.Faker('pt_BR')
        partner = self.env['res.partner']
        partner_dict = {}
        estado = self.env['res.country.state'].search(
            [('country_id', '=', 32)])
        estado = random.choice(estado)
        cidade = self.env['res.state.city'].search(
            [('state_id', '=', estado.id)])
        cidade = random.choice(cidade)
        telefone = fake.phone_number()
        telefone = re.sub('\D', '', telefone)
        partner_dict['zip'] = ''.join(
            [str(random.randint(0, 9)) for _ in range(8)])
        partner_dict['street'] = fake.street_name()
        partner_dict['number'] = str(random.randint(1, 700))
        partner_dict['street2'] = ' '.join(fake.words(6))
        partner_dict['district'] = fake.bairro()
        partner_dict['country_id'] = 32
        partner_dict['state_id'] = estado.id
        partner_dict['city_id'] = cidade.id
        partner_dict['website'] = fake.url()
        partner_dict['phone'] = telefone
        partner_dict['email'] = fake.email()
        if person:
            partner_dict['company_type'] = 'person'
            partner_dict['name'] = fake.name()
            partner_dict['cnpj_cpf'] = fake_cpf()
        else:
            partner_dict['company_type'] = 'company'
            partner_dict['name'] = fake.company()
            partner_dict['cnpj_cpf'] = fake_cnpj()
            partner_dict['is_company'] = True
        partner.create(partner_dict)

    def gen_products(self):
        fake = faker.Faker('pt_BR')
        product = self.env['product.product']
        price = float('{:.2f}'.format(random.uniform(5, 100)))
        prod_dict = {
            'name': ' '.join(fake.words(random.randint(1, 3))),
            'type': random.choice(['consu', 'service']),
            'list_price': price,
            'cost': 0,
        }
        product.create(prod_dict)

    @api.multi
    def populate(self):
        if self.generate_company:
            for _ in range(self.company_numbers):
                self.generate_client(person=False)
        if self.generate_fisical_partner:
            for _ in range(self.fisical_partner_number):
                self.generate_client()
        if self.generate_products:
            for _ in range(self.products_number):
                self.gen_products()
        if self.generate_my_company:
            self.generate_own_company()
        if self.generate_employees:
            for _ in range(self.employees_number):
                self.generate_user()
