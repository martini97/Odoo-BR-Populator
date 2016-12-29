# -*- coding: utf-8 -*-
# © 2016  Alessandro Fernandes Martini - TrustCode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Odoo BR Populator',
    'description': """\
Auto populador de bases para Odoo (localização brasileira)
    - Cria pessoas físicas e jurídicas
    - Cria produtos
    - Cria usuários
    - Configura a empresa
Todos os objetos são criados já configurados para a localização brasileira,
com CPF/CNPJ, CEP, endereço, email, telefone, etc.""",
    'license': 'AGPL-3',
    'author': 'TrustCode',
    'website': 'http://trustcode.com.br/',
    'version': '0.0.1',
    'external_dependencies': {
        'python': ['faker'],
    },
    'data': ['wizard/populator_wizard.xml', ],
    'category': 'Localisation',
    'auto_install': True,
}
