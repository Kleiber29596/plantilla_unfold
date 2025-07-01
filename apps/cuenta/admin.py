from django.contrib             import admin
from django.contrib.auth.admin  import UserAdmin
from django.contrib.auth.forms  import UserCreationForm

from django.utils.html 			import format_html

from .models                    import *

from django.contrib.auth.models import Group
#admin.site.unregister(Group)

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email',)


class CustomUserAdmin(UserAdmin):
    # Accesos directos del lado derecho
    def editar(self, obj):
        return format_html('<a class="btn" href="/admin/cuenta/user/{}/change/"><i class="nav-icon fas fa-edit"></i></a>', obj.id)
    
    def eliminar(self, obj):
        return format_html('<a class="btn" href="/admin/cuenta/user/{}/delete/"><i class="nav-icon fas fa-trash"></i></a>', obj.id)


    def has_add_permission(self, request, obj=None):
        return True


    add_form            =   UserCreateForm
    prepopulate_fields  =   {'username': ('origen','cedula','email',)}
    add_fieldsets       =   (
                                (
                                    None,   {
                                                'classes': ('wide',),
                                                'fields': ('username','origen','cedula','nombre_apellido','email','password1','password2')
                                            }
                                ),
                            )
    readonly_fields     =   ['pregunta_01','pregunta_02','pregunta_03','respuesta_01','respuesta_02','respuesta_03','last_login','fecha_registro','fecha_actualizacion','is_superuser']
    list_display        =   ('username','cedula','email','editar')
    list_filter         =   ('username','cedula','email')
    search_fields       =   ()
    list_display_links  = None
    actions             = None

    fieldsets           =   (
                                ('Credenciales',    {'fields': ('username','origen','cedula','nombre_apellido','email','password')                          }),
                                ('Recuperación',    {'fields': ('pregunta_01','pregunta_02','pregunta_03','respuesta_01','respuesta_02','respuesta_03',)    }),
                                ('Permisos',        {'fields': ('is_staff','is_active')                                                                     }),
                                ('Grupos',          {'fields': ('groups',)                                                                                  }),
                                ('Actividad',       {'fields': ('fecha_registro','fecha_actualizacion','last_login',)                                       }),
                            )
    class Media:
        js = ('js/autocompletar_cargo.js',)

        
admin.site.register(User,       CustomUserAdmin)