# Projeto 2 – Predizendo Prognóstico de Mortalidade com Dados Sintéticos

# Apresentação

O presente projeto foi originado no contexto das atividades da disciplina de pós-graduação [*Ciência e Visualização de Dados em Saúde*](https://ds4h.org), oferecida no primeiro semestre de 2022, na Unicamp.

|Nome  | RA | Especialização|
|--|--|--|
| Guilherme Augusto Amorim Terrell  | 168899  | Elétrica|
| Matheus Xavier Sampaio  | 220092  | Computação|

# Contextualização da Proposta
Analisando um conjunto de variáveis de pacientes que deram entrada em uma unidade de saúde, deseja-se construir um modelo de machine learning capaz de prever se o paciente virá a óbito em até um ano após a última vez que deu entrada.

Abaixo temos uma listagem com as variáveis que foram escolhidas para alimentar o modelo de machine learning proposto nesse projeto. Essas variáveis foram selecionadas pois apresentam alguma relação direta com o estado de saúde atual do paciente, e terão relevância caso esse paciente necessite de atendimento médico. Por exemplo, um paciente que possui algum tipo de alergia severa ou que faz uso de medicamento controlado pode ter mais chance de vir a óbito em caso de emergência médica. Um indivíduo que possui plano de saúde pode ter mais chance de sobreviver a uma intervenção médica do que um indivíduo que não possui plano de sáude.

### Variáveis usadas para prognóstico

- Informações gerais do paciente (`patients.csv`: `birthdate`, `deathdate`, `race`, `ethnicity`, `gender`, `city`, `state`)
- Tipo de entrada (`encounters.csv`: `start`, `stop`, `patient`, `encounterclass`, `code`, `description`)
- Condição de chegada (`conditions.csv`: `start`, `stop`, `patient`, `encounter`, `code`, `description`)
- Tem plano de saúde (`careplans.csv`: `start`, `stop`, `patient`, `encounter`, `code`, `description`)
- Imunização do paciente (`immunizations.csv`: `date`, `patient`, `encounter`, `code`, `description`)
- Gravidade de alergia (`allergies.csv`: `start`, `stop`, `patient`, `encounter`, `category`, `description1`, `severity1`, `description2`, `severity2`)
- Medicamentos tomados (`medications.csv`: `start`, `stop`, `patient`, `encounter`, `code`, `description`)
- Tem disposivo médico implantado (`devices.csv`: `start`, `stop`, `patient`, `encounter`, `code`, `description`)
- Realizou algum procedimento médico (`procedures.csv`: `start`, `stop`, `patient`, `encounter`, `code`, `description`)
- Médidas de observação (`observations.csv`: `date`, `patient`, `encounter`, `code`, `description`, `value`, `units`, `type`)


## Ferramentas
O projeto foi todo desenvolvido em linguagem de programação Python na plataforma Google Colaboratory.
As principais bibliotecas e módulos do python utilizados nesse projeto foram:

*   Importação e tratamento dos dados:
    *   pandas;
    *   numpy;

*   Implementação do modelo de machine learning:
    *   sklearn.model_selection;
    *   skleran.preprocessing;
    *   sklearn.tree;

*   Visualização e avaliação dos resultados:
    *   matplotlib;
    *   seaborn;
    *   sklearn.metrics;

# Metodologia
Implementaremos funções que coletem, em cada uma das bases de dados, informações específicas de cada paciente e gere uma coluna para cada resultado preenchida com o valor encontrado ou com "NaN" caso o paciente não tenha aquele registro específico. Dessa forma, teremos ao final um dataframe cujas linhas são um encontro, ou visita do paciente a unidade de saúde, e as colunas são as features, ou informações referentes ao paciente no momento do encontro que alimentaram o modelo de aprendizado de máquina. Nesse projeto o modelo escolhido foi o de árvore de decisão.

A princípio não será rejeitada nenhuma feature, apenas após rodarmos o algorítmo ao menos uma vez analisaremos as variáveis que não tiveram uma relevância mínima na predição e as removeremos.

## Bases Adotadas para o Estudo

* scenario01
* scenario02

# Evolução do Projeto
A idéia inicial era fazer o prognóstido se o paciente viria a óbito 30 dias após o encontro, no entanto, a quantidade de encontros que respeitam esta condição é muito pequena. Assim o prognóstico será se o paciente virá a óbito 1 ano após o encontro.

# Discussão
O modelo de prognóstico treinado obteu uma acurácia de $97\%$. No entanto, este é um problema que possui um grande desbalanceamento de classes. No conjunto de testes, apenas $6\%$ das classes pertencem ao grupo de pacientes que não sobrevivem até 1 ano. Assim, as métricas de precisão, revocação e f1 são mais importantes para avaliar o desempenho do modelo.

Nestas métricas, o modelo atinge $0.71$ na precisão, $0.78$ na revocação e $0.75$ no f1. Estas métricas mostram que o modelo conseguiu aprender as caracteristicas do conjunto de treino e usou este aprendizado no conjunto de treino de forma satisfatória, mas com boa margem para melhoria.

Vemos pelas métricas apresentadas que ao treinar o modelo apenas no cenário 1, o seu aprendizado não foi transferido ao aplicar no cenário 2. Teorizamos que isso se dá devido a diferenças econômicas, demográficas e geográficas entre pacientes nos dois cenarios. Podemos observar também que a feature mais importante foi a de planos de saúde, o que faz sentido, uma vez que as duas cidades analisadas localizam-se nos EUA, onde não há um sistema de saúde público como o SUS, portanto a quantidade de dinheiro que um indivíduo investiu em planos de saúde é uma variável importate no contexto desse projeto.

# Conclusão
A principal difuculdade desse projeto foi conseguir unir todos os conjuntos de dados (alergia, plano de saúde, etc) em um único dataset, de modo que cada feature representasse uma coluna e cada valor fosse associado ao seu respectivo ID.

Como melhoria podemos implementar diferentes técnicas de aprendizagem de máquina (random forest, KNN, regressão logística) e avaliar qual delas teve melhor desempenho. Além disso, dispondo de mais tempo para a enterega do projeto, podemos implementar uma análise exploratória mais robusta a fim de compreender melhor a distribuição dos dados e identificar possíveis outliers.