from models import PerfilUsuario

PERMISSOES = {

    PerfilUsuario.ADMINISTRADOR: {
        "usuarios",
        "ubs",
        "medicamentos",
        "estoques",
        "movimentacoes",
        "logs",
        "configuracoes"
    },

    PerfilUsuario.GESTOR: {
        "ubs",
        "medicamentos",
        "estoques",
        "movimentacoes",
        "logs"
    },

    PerfilUsuario.FARMACEUTICO: {
        "estoques",
        "movimentacoes"
    },

    PerfilUsuario.ATENDENTE: {
        "consulta"
    },

    PerfilUsuario.CONSULTA: {
        "consulta"
    }

}