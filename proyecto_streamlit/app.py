# Importacion de librerias
import streamlit as st
import pandas as pd
import altair as alt

# Set page config
st.set_page_config(
    page_title='Proyecto Final', # Titulo de la pagina
    page_icon='📊', # Icono de la pagina
    layout='wide', # Ancho de la pagina (wide, center)
    initial_sidebar_state='expanded', # Estado inicial del sidebar (expanded, collapsed)
    
)


# Sidebar
st.sidebar.title("Proyecto final Bootcamp de Ciencia de Datos")
st.sidebar.markdown(
    """
    Puedes utilizar el selector de esta barra para cambiar en tiempo real
    los valores a utilizar de uno o más meses.
    >**Nota:** El dataset contiene datos del segundo semestre del año 2010.
    Para una mejor visualización inicial se recomienda seleccionar todos los meses que vienen en el selector.
    """
)

# Intro section
st.title("Exploración de datos de créditos Bancarios en su proceso de cobranza en el año 2010.")
st.write(
    """
     Bienvenid@, este es mi proyecto final del bootcamp de ciencia de datos en código facilito.
    """
)

# Context
st.header("Contexto")
st.markdown(
    """
La empresa es una agencia de cobranza con más de 15 años en el mercado, teniendo a diferentes clientes de distintos giros pero con una caracteristica en común, que cada empresa tiene la posibilidad de otrogar créditos, créditos de los cuales se realiza el proceso de cobranza.

Cobranza: La cobranza es el acto o procedimiento por el cual se consigue la contraprestación por un bien o servicio o la cancelación de una deuda.

Referencia: https://economipedia.com/definiciones/cobranza.html

Para este proyecto nos enfocaremos en analizar la información de contacto con el deudor, dicho de otra manera, la gestión de la cuenta.

El objetivo final de cada gestión realizada a una cuenta es conseguir una promesa de pago por parte del titular.

Una promesa de pago es el registro de la fecha en que el titular se compromete a realizar el pago solicitado.

Dados estos escenarios, las preguntas que buscamos responder son las siguientes:

1. ¿Que cantidad de Gestiones se realizan en periodos de 1 mes?

1. ¿Que cantidad de promesas de pago se consiguieron en periodos de 1 mes?

1. ¿Hay relación entre el volumen de Gestiones y la cantidad de promesas de pago?

Palabras clave: gestión, promesa de pago
    """
)


# Load data
data = pd.read_csv('data/gestiones_bnx_filtradas.csv')

st.header("Cargando los datos")
st.markdown(
    """
    A continuación cargamos los datos (originales) a utilizar. Dichos datos pueden ser encontrados en la carpeta de datos como `data/gestiones_bnx_filtradas.csv`.
    Estos fueron previamente filtrado de una base de datos, los datos tienen campos utilies para la gestión, más no datos de las cuentas.
    Después del filtrado se obtuvieron un total de 1,028,390 registros de gestiones que pertenecen a un universo de cuentas de 102,033.

>**Nota**: Los datos y el código fuente de esta aplicación web pueden 
>ser encontrados en el repositorio de GitHub.

>Los datos pueden ser cargados utilizando pandas con las líneas:

```python
import pandas as pd
data = pd.read_csv('data/gestiones_bnx_filtradas.csv')
```

> **Nota:** Para desplegar los datos en pantalla, puedes llamar directamente a la variable
> desde una celda si usas  Google Colab que fue en donde trabaje el proyecto.
> ```python
># Desde un notebook
>data
>```

Al desplegar los datos deberías ver una tabla como la siguiente:
""")

st.dataframe(data)
st.markdown(
    """
    Podemos ver que nuestros datos tiene en total `10 columnas y 1,028,390 registros de gestiones`.

    Para este análisis solamente utilizaremos los campos: `Fecha, IdCodResultado`.

    | Campo       | Descripción    |
    |    :----:   |          :---: |
    | Fecha       | Fecha en que se realizo la gestión   |
    | IdCodResultado       | Id que identifica el resultado de una gestión      |
    | IdCtaDesp | Id asignado por software de cobranza a una cuenta|

    En el sistema que recopila la información existe un catalogo de resultados de gestión, por ejemplo: 
    - No contesta
    - Ausente

    El que utilizaré para este análisis es el IdCodResultado=49 y IdCodResultado=82,`estos códigos son asignado por el sistema de información utilizado por la agencia`.

    Para poder filtrar los datos a visualizar por mes, le agregamos la columna `Mes` al dataset original

    ```python
    # Crear columna de mes para poder filtrar la informacion
    data['Fecha'] = pd.to_datetime(data['Fecha'])
    data.insert(0,'Mes', (data['Fecha'].dt.month).astype(int) )

    # Creacion de list para el selector
    list_meses = data['Mes'].unique()
    list_meses.sort()

    mes = st.sidebar.multiselect('Seleccione el Mes', list_meses, list_meses[0])

    # dataframe filtrado 
    data_filter = data[
        (data['Mes'].isin(mes))
    ]

    Lo ponemos en la primer columna para visualizar el cambio de seleccion
    ```
    """
)
# Crear columna de mes para poder filtrar la informacion
data['Fecha'] = pd.to_datetime(data['Fecha'])
data.insert(0,'Mes', (data['Fecha'].dt.month).astype(int) )

# Creacion de list para el selector
list_meses = data['Mes'].unique()
list_meses.sort()

mes = st.sidebar.multiselect('Seleccione el Mes', list_meses, list_meses[:])

# dataframe filtrado 
data_filter = data[
    (data['Mes'].isin(mes))
]

st.write(data_filter)

# Imputación de datos
st.header("Imputación de datos")
st.markdown(
    """
    Dadas las reglas de negocio que están implementadas en el software que se utiliza
    para el proceso de cobranza, las columnas que utilizaremos no contienen valores nulos o vacios.

    **Regla de registro de gestion:** Una gestión siempre deberá tener fecha y un resultado.
    """    
)


# Gráficas Containner principal
with st.container():
    # Titulo
    st.title('Visualización de datos')
    st.markdown(
        """
        Para poder grágicar las `promesas de pago` por mes vamos a crear un nuevo dataframe que solo contenga la fecha y el resultado.
        """
    )

df_fecha_codResultado = data_filter[['Fecha','IdCodResultado']]

st.write(df_fecha_codResultado)

st.markdown(
    """
    Despues hacemos un crosstab para agruparlo por mes, en donde las columnas pasan a ser los IdCodResultado
    """
)


df_fecha_codResultado.Fecha = pd.to_datetime(df_fecha_codResultado.Fecha,dayfirst=True)
df_fecha_codResultado.IdCodResultado = df_fecha_codResultado['IdCodResultado'].astype('string')

# Filtramos para solo tener las promesas de pago
df_promesas = df_fecha_codResultado[df_fecha_codResultado.IdCodResultado.isin(['49','82'])]



if df_promesas.empty == False:

    df_promesas_group = pd.crosstab(df_promesas.Fecha, df_promesas.IdCodResultado).resample("M").sum().reset_index()
    # Creamos una nueva columna donde sumamos los valores de la columna 49 y 82 que el sistema de informacion tiene identificado como promesa de pago
    df_promesas_group['sum_promesas'] = df_promesas_group['49'] + df_promesas_group['82']

    st.write(df_promesas_group)
    c = alt.Chart(df_promesas_group).mark_bar().encode(
        y= alt.Y("sum_promesas", title="Promesas"),
        x= alt.X("Fecha", title = "",timeUnit='month'),
        color = alt.Color("sum_promesas", title = "Volumen", scale = alt.Scale( scheme = "blues")),
    ).properties(
        title="Promesas de pago en el segundo semestre del año 2010"
    )
    text_line = c.mark_text(
        dx=35,
        dy=-15
    ).encode( 
        text=alt.Text('sum_promesas',format=",.0f") 
    )

    c1 = c+text_line

    st.altair_chart(c1.properties(
        width=490,
        height=330
    ).configure_title(
        fontSize=15,
        dy= -15
    ), use_container_width=True)
else:
    st.markdown(
        """
        >**El mes o meses seleccionados no contiene promesas de pago para gráficar**
        """
        )

st.markdown(
    """
    Con el trabajo que hemos realizado hasta este punto ya pudimos identificar el `mes en el que se registraron más promesas de pago`, que fue `Agosto con un total de 5,402`.

    El paso siguiente es saber el volumen de gestiones totales en comparacion con la cantidad de promesas de pago
    """
)

# Obtenemos los totales por mes de todos los codigos de resultado
df_totales = pd.crosstab(df_fecha_codResultado.Fecha,df_fecha_codResultado.IdCodResultado,dropna=True).resample("M").sum().reset_index()
df_totales.loc['total_gestiones', :] = df_totales.sum(numeric_only=True)
df_totales['total_gestiones'] = df_totales.sum(axis=1, numeric_only=True)
df_totales['sum_promesas'] = df_promesas_group['49'] + df_promesas_group['82']

df_totales_filter = df_totales[['Fecha','sum_promesas','total_gestiones']].query('total_gestiones > 0')
st.write(df_totales_filter)


# Creamos los objetos para graficar
scale = alt.Scale(domain=["Promesas","Gestiones"], range=['blue','gray'])

if df_promesas.empty == False:
    base = alt.Chart(df_totales).transform_calculate(
        line="'Promesas'",
        bar="'Gestiones'"
    ).encode(
        alt.X("Fecha",title="",timeUnit='month'),
    ).properties(
        title="Volumen de gestiones y cantidad de promesas conseguidas"
    )

    bar = base.mark_bar().encode(
        alt.Y('total_gestiones',title="Gestiones"),
        tooltip=[alt.Tooltip("total_gestiones", title='Gestiones')],
        color=alt.Color('bar:N', scale=scale, title=''),
    )

    line = base.mark_line(point=alt.OverlayMarkDef(color="red")).encode(
        alt.Y("sum_promesas",title=""),
        tooltip=[alt.Tooltip('sum_promesas',title='Promesas')],
        color=alt.Color('line:N', scale=scale, title='')
    )

    text_line = line.mark_text(
        align='right',
        baseline='bottom',
        dx=3
    ).encode( 
        text='sum_promesas'
    )

    text_bar = bar.mark_text(
        dx=35,
        dy=-15
    ).encode( 
        text=alt.Text('total_gestiones',format=",.0f") 
    )
    c = (bar+text_bar)+(line+text_line)

    st.altair_chart(c.properties(
        width=490,
        height=330
    ).configure_title(
        fontSize=15,
        dy= -15
    ),use_container_width=True)

    st.markdown(
        """
        Con la siguiente gráfica podemos observar lo siguiente:

        1. El volumen de gestiones es abismalmente superior a la cantidad de promesas de pago generadas en cada mes.

        2. El volumen de gestiones no siempre es proporcional a la cantidad de promesas de pago obtenidas. 
        En el mes de Septiembre se obtuvieron un total de 4,372 promesas de pago con un volumen de gestiones de 217,595, en el mes de Octubre se obtuvieron 4,439 con un volumen de 192,522.

        # Conclusiones - Primera parte
        >En este punto ya podemos contestar las preguntas que planteamos al principio.
        >
        >1. ¿Que cantidad de Gestiones se realizan en periodos de 1 mes?
        >2. ¿Que cantidad de promesas de pago se consiguieron en periodos de 1 mes?
        >**R= se puede visualizar en la gráfica "Volumen de gestiones y cantidad de promesas conseguidas"**
        >
        >3. ¿Hay relación entre el volumen de Gestiones y la cantidad de promesas de pago? 
        >**R= con los datos que se tienen hasta el momento no se observa una relación que nos indique que a mayor volumen de gestiones mayor cantidad de promesas de pago se van a obtener, claro que esto es forma general.**
        """
        )
else:
    st.markdown(
        """
        >**El mes o meses seleccionados no contiene promesas de pago para gráficar**
        """
        )

st.markdown(
    """
    # Segunda parte

    Con el análisis anterior, surgieron nuevas preguntas las cuales podrían esclarecer la manera en que se trata a una cuenta.

    Las preguntas que surgieron fueron las siguientes:

    1. ¿Que cantidad de gestiones recibe en promedio una cuenta?

    1. ¿En periodos de 1 mes se llega a gestionar todas las cuentas?
    """
)

# Creamos una copia del dataframe original
df_copy = data_filter
# Convertimos el campo a datetime
df_copy.Fecha = pd.to_datetime(df_copy.Fecha,dayfirst=True)

# Convertimos a entero el la fecha y la insertamos en una nueva columna llamada Mes
# df_copy.insert(0,'Mes', (data['Fecha'].dt.month).astype(int) )

# Agrupamos primero por mes y despues por IdCtaDesp para no hacer un conteo doble de gestiones
df_gestiones_promedio = df_copy.groupby(['Mes','IdCtaDesp'],as_index=False).IdCtaDesp.count()

st.markdown(
    """
    Agrupamos primero por mes y despues por IdCtaDesp
    ```python
    df_gestiones_promedio = df_copy.groupby(['Mes','IdCtaDesp'],as_index=False).IdCtaDesp.count()
    ```
    """
)
st.write(df_gestiones_promedio)

# Agrupamos por el mes, agregando el promedio del campo IdCTaDesp que contiene el total de gestiones y los redondeamos
df_promedio_final = df_gestiones_promedio.groupby(['Mes'],as_index=False).mean('IdCtaDesp').round()

# Convertimos el mes a texto para mejor visualización al momento de generar el gráfico
df_promedio_final['Mes'] = pd.to_datetime(df_promedio_final['Mes'], format='%m').dt.strftime('%b')

df_promedio_final =df_promedio_final.sort_index()

st.markdown(
    """
    
    ```python
    # Agrupamos por el mes, agregando el promedio del campo IdCTaDesp que contiene el total de gestiones y los redondeamos
    df_promedio_final = df_gestiones_promedio.groupby(['Mes'],as_index=False).mean('IdCtaDesp').round()

    # Convertimos el mes a texto para mejor visualización al momento de generar el gráfico
    df_promedio_final['Mes'] = pd.to_datetime(df_promedio_final['Mes'], format='%m').dt.strftime('%b')
    ```
    """
)
st.write(df_promedio_final)

# Promedio de gestiones realizadas a una cuenta por mes
 
bar = alt.Chart(df_promedio_final).mark_bar().encode(
    y= alt.Y("IdCtaDesp", title="Gestiones"),
    x= alt.X("Mes", title = "",sort=['Mes']),
    color = alt.Color('IdCtaDesp', title = "Gestiones", scale = alt.Scale( scheme = "blues")),
    tooltip=[alt.Tooltip('IdCtaDesp',title="Gestiones")]
).properties(
    title="Promedio de gestiones por cuenta",
    width = 450
)

text_c1 = bar.mark_text(
    dx=0,
    dy=-15
).encode( 
    text=alt.Text('IdCtaDesp',format=",.0f") 
)

c1 = bar+text_c1

line = base.mark_line(point=alt.OverlayMarkDef(color="red")).encode(
    alt.Y("sum_promesas",title=""),
    tooltip=[alt.Tooltip('sum_promesas',title='Promesas')],
    color=alt.Color('line:N', scale=scale, title='')
)

text_line = line.mark_text(
    align='right',
    baseline='bottom',
    dx=3
).encode( 
    text='sum_promesas'
)

c2 = line+text_line

combined = (c1 | c2)

st.altair_chart(combined, use_container_width=True)

# En el dataFrame df_gestiones_promedio ya teniamos agrupadas las cuentas, entonces se eliminaron los duplicados
# por lo cual vamos a hacer el conteo en vez del promedio para saber que cantidad de cuentas se gestionan en periodos de 1 mes
df_ctas_mes = df_gestiones_promedio.groupby(['Mes'],as_index=False).count()

df_ctas_mes['Mes'] = pd.to_datetime(df_ctas_mes['Mes'], format='%m').dt.strftime('%b')

st.markdown(
    """
    Obteniendo el promedio de gestiones que recibe una cuenta en un mes, podemos observar que va en aumento, sin embargo las promesas obtenidas no son proporcionales, lo que pudiera indicarnos `que la insistencia en la cobranza no siempre es la clave para conseguir una promesa de pago`, esto considerando que la mayor parte de las cuentas recibiera una gestión, sin embargo, en la Gráfica 2 se observa que el volumen de gestiones disminuye.
    ```python
    # En el dataFrame df_gestiones_promedio ya teniamos agrupadas las cuentas, entonces se eliminaron los duplicados
    # por lo cual vamos a hacer el conteo en vez del promedio para saber que cantidad de cuentas se gestionan en periodos de 1 mes
    df_ctas_mes = df_gestiones_promedio.groupby(['Mes'],as_index=False).count()

    df_ctas_mes['Mes'] = pd.to_datetime(df_ctas_mes['Mes'], format='%m').dt.strftime('%b')

    df_ctas_mes
    ```
    """
)

st.write(df_ctas_mes)

# importamos spacing de numpy para la separación de gráficas
from numpy import spacing

bar = alt.Chart(df_ctas_mes).mark_bar().encode(
    y= alt.Y("IdCtaDesp", title="Cuentas"),
    x= alt.X("Mes", title = "",sort=['Mes']),
    color = alt.Color('IdCtaDesp', title = "Cuentas", scale = alt.Scale( scheme = "blues")),
    tooltip=[alt.Tooltip('IdCtaDesp',title="Cuentas")]
).properties(
    title="Total de Cuentas Gestionadas por mes",
    width=500
)

text_c1 = bar.mark_text(
    dx=0,
    dy=-15
).encode( 
    text=alt.Text('IdCtaDesp',format=",.0f") 
)

c1 = bar + text_c1

bar = alt.Chart(df_totales).mark_bar().encode(
    alt.X("Fecha",title="",timeUnit='month'),
    alt.Y('total_gestiones',title="Gestiones"),
    # color = alt.Color('total_gestiones', title = "Gestiones", scale = alt.Scale( scheme = "teals")),
).properties(
    title="Volumen de Gestiones por mes",
    
)

text_c2 = bar.mark_text(
    dx=35,
    dy=-15
).encode( 
    text=alt.Text('total_gestiones',format=",.0f") 
)

c2 = bar + text_c2

combined = alt.hconcat(
    c1.properties(
        width=490,
        height=330), 
    c2.properties(
        width=490,
        height=330
    )
).resolve_scale(
    color='independent'
).properties(
    spacing=100
)

st.altair_chart(combined, use_container_width=True)

st.markdown(
    """
    Con las gráficas anteriores podemos ver que la cantidad de cuentas gestionadas decrementa al igual que el volumen de gestiones en cada uno de los periodos, entonces empezamos a tener `menos cuentas gestionadas, menos volumen de gestiones y el promedio de gestiones por cuenta aumenta.`


    # Conclusiones - Segunda Parte
    Las preguntas que surgieron fueron las siguientes:

    1. ¿Que cantidad de gestiones recibe en promedio una cuenta?
    **R= rango de 2 a 7 en el semestre**
    1. ¿En periodos de 1 mes se llega a gestionar todas las cuentas?
    **R= No, la campaña de cobranza no llega a todo el universo de cuentas**

    Para complementar las respuestas a las interrogantes se deben mencionar escenarios que pasan en la operacion de la agencia de cobranza, que son los siguientes:


    - **Disminución de cuentas a gestionar:** esta disminución de cuentas puede darse por que existen cuentas que su deuda puede quedar liquidada, al entrar en este estado ya no se contempla dentro del universo de cuentas a gestionar.

    - **Cantidad de gestiones por cuenta:** existen cuentas en las cuales obtienes una promesa de pago a la primer gestion, hay cuentas que hasta la *n* gestion obtienes una promesa de pago, estas gestiones previas a una promesa de pago se quedan registradas para que el la persona que interactue con el titular de la cuenta sepa el proceso de gestión de la misma.

    # Conclusión final


    Para complementar la conclusión final vamos a obtener la diferencia y el porcentaje de variación de uno de los puntos claves, las promesas de pago.
    ```python
    Utilizamos el dataframe donde hicimos la sumatoria de las promesas
    df_variacion = df_totales[['Fecha','sum_promesas']]

     utilizamos la funcion drop para eliminar la fila 0
     ya que la sumatoria de promesas no es significante en comparacion con los demas datos
    df_variacion.drop([0], axis=0, inplace=True) 

    ```
    """
)

# Utilizamos el dataframe donde hicimos la sumatoria de las promesas
df_variacion = df_totales[['Fecha','sum_promesas']].reset_index()

# utilizamos la funcion drop para eliminar la fila 0
# ya que la sumatoria de promesas no es significante en comparacion con los demas datos
# df_variacion.drop(labels=0, axis=0,inplace=True) 
df_variacion.drop(0, axis=0, inplace=True) 
# df_variacion = df_variacion.drop([0], axis=0, inplace=True)
st.write(df_variacion)

# df_variacion.drop(labels=0, axis=0, inplace=True)

# df_variacion
st.markdown(
    """
     Creamos la columna diferencia por cada periodo
    ```python
        df_variacion['diferencia'] = df_variacion.sum_promesas.diff()
    ```
    """
)
# Creamos la columna diferencia por cada periodo
df_variacion['diferencia'] = df_variacion['sum_promesas'].diff()

st.write(df_variacion)

st.markdown(
    """
    Calculamos la variacion dividiendo la diferencia entre la suma de promesas de la fila anterior usando la función shift(1)
    ```python
    df_variacion['variacion'] = df_variacion.diferencia/df_variacion.sum_promesas.shift(1)*100
    ```
    """
)

df_variacion['variacion'] = df_variacion['diferencia']/df_variacion['sum_promesas'].shift(1)*100
st.write(df_variacion)

st.markdown(
    """
    La tendencia en promesas de pagos es a la baja, lo cual indicaría a simple vista que el proceso de cobranza no esta siendo efectivo, sin embargo hay que tomar en cuenta que la cantidad de cuentas gestionadas fue disminuyendo, lo cual nos generá más preguntas como: 

    1. ¿Cuales son los criterios para que una cuenta se elimine del universo de cuentas a ser gestionadas?

    2. El factor humano de la persona que realiza la campaña, ¿Que tanto unfluye? o si la empresa tiene un estandár de campañas de cobranza.

    Entre más "forma" van tomando los datos, más preguntas empiezan a surgir, entre más preguntas se vayan contestando, mejores decisiones se podrán tomar en caso contrario podemos saber que areas de oportunidad se tienen y trabajar en ello.
    """
)