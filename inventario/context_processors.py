# inventario/context_processors.py
def role_context(request):
    role = None
    if request.user.is_authenticated:
        perfil = getattr(request.user, 'perfil', None)
        role = getattr(perfil, 'rol', None)
    return {'role': role}

    TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # 👇 añade esta línea:
                'inventario.context_processors.role_context',
            ],
        },
    },
]

