"""
Dados de apoio de localidades brasileiras (cidade/UF).

Usado pelo gerador de dados fake, importador de CSV e scripts de manutenção.
Esta lista não tem TODAS as cidades do Brasil, mas traz várias
capitais, cidades grandes e cidades médias/menores por estado,
para deixar a distribuição de clientes mais realista.
"""

CIDADE_UF = {
    # Acre
    "Rio Branco": "AC",
    "Cruzeiro do Sul": "AC",
    "Sena Madureira": "AC",
    "Tarauacá": "AC",
    "Brasiléia": "AC",

    # Alagoas
    "Maceió": "AL",
    "Arapiraca": "AL",
    "Rio Largo": "AL",
    "Palmeira dos Índios": "AL",
    "Penedo": "AL",

    # Amapá
    "Macapá": "AP",
    "Santana": "AP",
    "Laranjal do Jari": "AP",

    # Amazonas
    "Manaus": "AM",
    "Parintins": "AM",
    "Itacoatiara": "AM",
    "Manacapuru": "AM",
    "Coari": "AM",

    # Bahia
    "Salvador": "BA",
    "Feira de Santana": "BA",
    "Vitória da Conquista": "BA",
    "Camaçari": "BA",
    "Itabuna": "BA",
    "Ilhéus": "BA",
    "Juazeiro": "BA",
    "Lauro de Freitas": "BA",
    "Barreiras": "BA",
    "Teixeira de Freitas": "BA",

    # Ceará
    "Fortaleza": "CE",
    "Sobral": "CE",
    "Juazeiro do Norte": "CE",
    "Maracanaú": "CE",
    "Caucaia": "CE",
    "Crato": "CE",
    "Iguatu": "CE",
    "Itapipoca": "CE",
    "Quixadá": "CE",
    "Canindé": "CE",

    # Distrito Federal
    "Brasília": "DF",
    "Taguatinga": "DF",
    "Ceilândia": "DF",
    "Gama": "DF",
    "Planaltina": "DF",

    # Espírito Santo
    "Vitória": "ES",
    "Vila Velha": "ES",
    "Serra": "ES",
    "Cariacica": "ES",
    "Linhares": "ES",
    "Cachoeiro de Itapemirim": "ES",
    "Colatina": "ES",
    "São Mateus": "ES",

    # Goiás
    "Goiânia": "GO",
    "Aparecida de Goiânia": "GO",
    "Anápolis": "GO",
    "Rio Verde": "GO",
    "Luziânia": "GO",
    "Águas Lindas de Goiás": "GO",
    "Formosa": "GO",
    "Trindade": "GO",
    "Catalão": "GO",

    # Maranhão
    "São Luís": "MA",
    "Imperatriz": "MA",
    "Caxias": "MA",
    "Timon": "MA",
    "Açailândia": "MA",

    # Mato Grosso
    "Cuiabá": "MT",
    "Várzea Grande": "MT",
    "Rondonópolis": "MT",
    "Sinop": "MT",
    "Cáceres": "MT",

    # Mato Grosso do Sul
    "Campo Grande": "MS",
    "Dourados": "MS",
    "Três Lagoas": "MS",
    "Corumbá": "MS",
    "Ponta Porã": "MS",

    # Minas Gerais
    "Belo Horizonte": "MG",
    "Contagem": "MG",
    "Betim": "MG",
    "Uberlândia": "MG",
    "Juiz de Fora": "MG",
    "Uberaba": "MG",
    "Montes Claros": "MG",
    "Governador Valadares": "MG",
    "Ipatinga": "MG",
    "Divinópolis": "MG",
    "Poços de Caldas": "MG",

    # Pará
    "Belém": "PA",
    "Ananindeua": "PA",
    "Santarém": "PA",
    "Marabá": "PA",
    "Castanhal": "PA",
    "Abaetetuba": "PA",

    # Paraíba
    "João Pessoa": "PB",
    "Campina Grande": "PB",
    "Patos": "PB",
    "Sousa": "PB",
    "Cajazeiras": "PB",
    "Guarabira": "PB",

    # Paraná
    "Curitiba": "PR",
    "Londrina": "PR",
    "Maringá": "PR",
    "Ponta Grossa": "PR",
    "Cascavel": "PR",
    "Foz do Iguaçu": "PR",
    "Guarapuava": "PR",
    "Paranaguá": "PR",
    "Colombo": "PR",

    # Pernambuco
    "Recife": "PE",
    "Olinda": "PE",
    "Jaboatão dos Guararapes": "PE",
    "Caruaru": "PE",
    "Petrolina": "PE",
    "Garanhuns": "PE",
    "Paulista": "PE",

    # Piauí
    "Teresina": "PI",
    "Parnaíba": "PI",
    "Picos": "PI",
    "Floriano": "PI",

    # Rio de Janeiro
    "Rio de Janeiro": "RJ",
    "Niterói": "RJ",
    "Duque de Caxias": "RJ",
    "Nova Iguaçu": "RJ",
    "Petrópolis": "RJ",
    "Volta Redonda": "RJ",
    "Campos dos Goytacazes": "RJ",
    "São Gonçalo": "RJ",
    "Cabo Frio": "RJ",

    # Rio Grande do Norte
    "Natal": "RN",
    "Mossoró": "RN",
    "Parnamirim": "RN",
    "Caicó": "RN",

    # Rio Grande do Sul
    "Porto Alegre": "RS",
    "Caxias do Sul": "RS",
    "Pelotas": "RS",
    "Santa Maria": "RS",
    "Canoas": "RS",
    "Passo Fundo": "RS",
    "Novo Hamburgo": "RS",
    "São Leopoldo": "RS",
    "Rio Grande": "RS",
    "Gramado": "RS",

    # Rondônia
    "Porto Velho": "RO",
    "Ji-Paraná": "RO",
    "Ariquemes": "RO",
    "Vilhena": "RO",
    "Cacoal": "RO",

    # Roraima
    "Boa Vista": "RR",
    "Rorainópolis": "RR",

    # Santa Catarina
    "Florianópolis": "SC",
    "Joinville": "SC",
    "Blumenau": "SC",
    "Itajaí": "SC",
    "Chapecó": "SC",
    "Criciúma": "SC",
    "Lages": "SC",
    "Balneário Camboriú": "SC",

    # São Paulo
    "São Paulo": "SP",
    "Campinas": "SP",
    "Santos": "SP",
    "Sorocaba": "SP",
    "Ribeirão Preto": "SP",
    "São José dos Campos": "SP",
    "São Bernardo do Campo": "SP",
    "Santo André": "SP",
    "Guarulhos": "SP",
    "Osasco": "SP",
    "São José do Rio Preto": "SP",
    "Piracicaba": "SP",
    "Bauru": "SP",
    "Franca": "SP",
    "Jundiaí": "SP",
    "Mogi das Cruzes": "SP",
    "Diadema": "SP",
    "Barueri": "SP",

    # Sergipe
    "Aracaju": "SE",
    "Nossa Senhora do Socorro": "SE",
    "Lagarto": "SE",
    "Itabaiana": "SE",

    # Tocantins
    "Palmas": "TO",
    "Araguaína": "TO",
    "Gurupi": "TO",
    "Porto Nacional": "TO",
}

CIDADES = list(CIDADE_UF.keys())
UFS = sorted(set(CIDADE_UF.values()))
