# -*- coding: utf-8 -*-


from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

if not request.is_local:
    from gluon.contrib.login_methods.ldap_auth import ldap_auth
    auth.settings.login_methods=[ldap_auth(mode='uid',server='ldap.unirio.br', base_dn='ou=people,dc=unirio,dc=br')]

db.define_table('edicao',
                Field('nome', 'string', notnull=True, required=True, label='Edital*'),
                Field('dt_inicial', 'date', notnull=True, required=True, label='Data inicial*'),
                Field('dt_conclusao', 'date', notnull=True, required=True, label="Data final*"),
                Field('disciplinas_obrigatorias', 'boolean', notnull=True, required=True, label='Mostrar somente disciplinas obrigatórias?*'))

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
