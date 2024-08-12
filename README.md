**Você foi contratado pela Plácido Drive para testar o sistema de armazenamento de arquivos do Professor Plácido para a turma da disciplina de testes de software. Seu objetivo é encontrar possíveis falhas de segurança no sistema. Prepare-se para um desafio que pode revelar algumas surpresas!**

**Questão 1:** Imagine que você é um detetive da segurança e conseguiu se infiltrar no sistema da Plácido Drive. Utilize um SQL Injection para acessar a lista de todos os usuários. Seu objetivo é verificar se há algum usuário que não deveria estar lá. _Dica: existe um endpoint que deveria retornar os dados só do seu usuário, mas se usado corretamente poderá trazer informações que deveriam ser sigilosas!_

- Qual o nome completo do nosso invasor?

**Questão 2:** Você descobriu um usuário que parece estar fora do lugar. Agora, é hora de agir como um verdadeiro "hacker ético". Altere a senha desse usuário para conseguir acessar o arquivo que ele salvou no servidor. Para isso ainda é preciso encontrar qual o nome de usuário dele! _Dica: existe outro endpoint que expões uma vulnerabilidade de Command Injection, aproveite-se dessa falha para tentar encontra alguma pista por lá!_

- Qual foi a mensagem secreta deixada por ele?

**Questão 3:** Agora que você descobriu qual o username do usuário malicioso, encontre qual o arquivo que ele fez upload. Você precisa entrar na conta dele alterando a senha de acesso! _Dica: Existe uma grave falha na implementação da funcionalidade de alterar senha, talvez ela permita que você troque a senha do usuário!_

**Questão 4:** Agora é só entrar na conta do usuário malicioso, e fazer download do arquivo que ele enviou. Lá estará o código secreto para completar a tarefa!

- Qual foi a mensagem secreta final deixada pelo nosso invasor?
