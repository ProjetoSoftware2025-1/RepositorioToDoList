### 1\. Autenticação e Perfil

- **1.1. Cadastro e Login de Usuário**
  
  - **Descrição**: Validar o fluxo de registro de um novo usuário e seu login subsequente.
  - **Passos**:
        1. Acessar a página inicial.
        2. Clicar em "Inscreva-se aqui".
        3. Preencher todos os dados (nome completo, usuário, email, senha) e clicar em "CADASTRAR".
        4. Na página de login, usar as credenciais recém-criadas e clicar em "LOGIN".
  - **Resultado obtido**: Cadastro bem-sucedido, redirecionamento para a página de login, e login bem-sucedido para o Dashboard. Tentar login com credenciais inválidas deve mostrar mensagem de erro.
- **1.2. Atualização de Perfil e Logout**
  - **Descrição**: Verificar a atualização de dados do perfil e a função de logout.
  - **Pré-condições**: Usuário logado.
  - **Passos**:
        1. No Dashboard, clicar no avatar/nome de usuário na barra lateral para acessar "Atualizar Perfil".
        2. Alterar o "Usuário" e/ou "Email".
        3. Inserir uma "Nova senha" e "Confirmar senha" (certificando-se que elas são iguais).
        4. Clicar em "Salvar".
        5. Clicar em "Sair" na barra lateral.
  - **Resultado obtido**: Dados e/ou senha do perfil são atualizados com sucesso. O logout redireciona para a página de login com mensagem de sucesso.

### 2\. Gerenciamento de Tarefas

- **2.1. Criação e Visualização de Tarefa**
  
  - **Descrição**: Testar a criação de uma tarefa e a visualização de seus detalhes.
  - **Pré-condições**: Usuário logado.
  - **Passos**:
        1. Na barra lateral, clicar em "Tarefas".
        2. Clicar em "+ Criar Nova Tarefa".
        3. Preencher "Título", "Descrição", "Data de Vencimento" e selecionar "Categoria". Clicar "Salvar Tarefa".
        4. Na lista de tarefas, clicar na tarefa recém-criada.
  - **Resultado obtido**: A tarefa é criada e aparece na lista. Seus detalhes são exibidos corretamente ao clicar nela.
- **2.2. Atualização e Conclusão de Tarefa**
  - **Descrição**: Validar a modificação e a conclusão de uma tarefa.
  - **Pré-condições**: Pelo menos uma tarefa existente e não concluída (criada no 2.1).
  - **Passos**:
        1. Acessar os detalhes de uma tarefa (ver 2.1).
        2. Clicar em "✏️ Atualizar", alterar algum campo e clicar em "Salvar Alterações".
        3. Novamente nos detalhes da tarefa, clicar em "✅ Concluir" e confirmar.
  - **Resultado obtido**: A tarefa é atualizada com sucesso. Após a conclusão, ela é removida das listas de "Em Progresso" e o score do usuário (se houver liga) é atualizado.
- **2.3. Exclusão de Tarefa e Filtragem**
  - **Descrição**: Verificar a exclusão de tarefas e a funcionalidade de filtragem.
  - **Pré-condições**: Pelo menos uma tarefa existente (criada no 2.1).
  - **Passos**:
        1. Acessar os detalhes de uma tarefa.
        2. Clicar em "🗑️ Excluir" e confirmar.
        3. Na página "Lista de Tarefas", usar os filtros de "Data", "Status" e "Categoria" para pesquisar tarefas específicas.
  - **Resultado obtido**: A tarefa é removida da lista. Os filtros exibem apenas as tarefas correspondentes aos critérios de pesquisa.

### 3\. Gerenciamento de Ligas

- **3.1. Criação e Ingresso em Liga**
  
  - **Descrição**: Testar a criação de uma nova liga e o ingresso em uma liga existente.
  - **Pré-condições**: Usuário logado.
  - **Passos**:
        1. Na barra lateral, clicar em "Minhas Ligas".
        2. Clicar em "👊 Criar uma liga", preencher os campos e clicar "Criar Liga". (Anote o código de convite).
        3. Voltar para "Minhas Ligas".
        4. Clicar em "➕ Entrar em uma nova liga", inserir um código de convite válido (da liga criada no passo 2 ou de outra), e clicar "Entrar na Liga".
  - **Resultado obtido**: A liga é criada com sucesso, e o usuário consegue entrar na liga, sendo redirecionado para seus detalhes, que mostram a lista de participantes.

### 4\. Relatórios e Calendário

- **4.1. Visualização de Relatórios**
  
  - **Descrição**: Verificar a exibição das estatísticas e detalhamento de tarefas nos relatórios.
  - **Pré-condições**: Usuário logado, com tarefas criadas e/ou concluídas.
  - **Passos**:
        1. Na barra lateral, clicar em "Relatórios".
        2. Clicar nas opções de filtro (Todas, Concluídas, Em Progresso, Atrasadas, Pendentes) na seção "Detalhamento das Tarefas".
  - **Resultado obtido**: As estatísticas (concluídas, produtividade) são exibidas corretamente. A tabela de tarefas filtra os resultados conforme o status selecionado.
- **4.2. Visualização do Calendário**
  - **Descrição**: Validar a exibição do calendário e a visualização de tarefas por dia.
  - **Pré-condições**: Usuário logado, com tarefas com datas de vencimento.
  - **Passos**:
        1. Na barra lateral, clicar em "Calendário".
        2. Clicar em um dia no calendário que contenha tarefas.
  - **Resultado obtido**: O calendário é carregado com as tarefas marcadas nos dias correspondentes. Ao clicar em um dia, um modal exibe as tarefas daquele dia.

### 5\. Pomodoro

- **5.1. Funcionalidade do Pomodoro**
  
  - **Descrição**: Verificar o funcionamento básico do temporizador e a alternância de modos.
  - **Pré-condições**: Usuário logado.
  - **Passos**:
        1. Na barra lateral, clicar em "Pomodoro".
        2. Clicar em "Iniciar", depois em "Pausar", e novamente em "Iniciar".
        3. Clicar em "Cancelar".
        4. Clicar em "INTERVALO CURTO", depois "INTERVALO LONGO", e finalmente "FOCO".
  - **Resultado obtido**: O temporizador inicia, pausa e reseta corretamente. O tempo do temporizador muda adequadamente ao alternar entre os modos de foco e intervalo.
