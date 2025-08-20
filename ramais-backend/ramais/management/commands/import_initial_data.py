from django.core.management.base import BaseCommand
from django.db import transaction
from ramais.models import Funcionario, Departamento, Funcao, Unidade
import re


class Command(BaseCommand):
    help = 'Importa dados iniciais da tabela pessoas do SQL fornecido'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpa todos os dados antes de importar',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Limpando dados existentes...')
            Funcionario.objects.all().delete()
            Departamento.objects.all().delete()
            Funcao.objects.all().delete()
            Unidade.objects.all().delete()

        self.stdout.write('Iniciando importação dos dados...')
        
        # Dados automáticos extraídos do SQL
        dados_pessoas = self._get_sql_data()

        try:
            with transaction.atomic():
                self._import_data(dados_pessoas)
            self.stdout.write(
                self.style.SUCCESS('Importação concluída com sucesso!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro durante a importação: {str(e)}')
            )

    def _get_sql_data(self):
        
        sql_data = """INSERT INTO `pessoas` (`id`, `Ramal`, `Email`, `Nome`, `Funcao`, `Whatsapp`, `Departamento`, `Unidade`, `Skype`, `created_at`, `updated_at`) VALUES
        (1, '7223', 'almoxarifado@chiaperini.com.br', 'Rodrigo P', 'Almoxarifado', NULL, 'Almoxarifado', 'Chiaperini', NULL, NULL, '2023-08-30 17:19:16'),
        (2, '7317', NULL, 'Roberto M', NULL, '', 'Suppy chain', 'Chiaperini', NULL, NULL, NULL),
        (3, '7243', 'adenilson@chiaperini.com.br', 'Adenílson', 'Assistente Técnico', '981130849', 'Assistência Técnica', 'Chiaperini', 'adenilson.junior1', NULL, '2023-08-30 15:40:59'),
        (4, '7213', 'paulomarques@chiaperini.com.br', 'Paulo Marques', 'Assistente Técnico', '993219072', 'Assistência Técnica', 'Chiaperini', 'paulo.marques.1', NULL, '2023-08-30 17:12:24'),
        (5, '7272', NULL, 'Gabriel Escobar', 'Assistente Técnico', '993203752', 'Assistência Técnica', 'Chiaperini', NULL, NULL, '2023-11-29 19:28:16'),
        (6, '7344', NULL, 'Eliza', 'Assistente Técnica', NULL, 'Assistência Técnica', 'Chiaperini', NULL, NULL, '2023-11-29 19:27:18'),
        (8, '7350', NULL, 'Gabriel Balbão', 'Assistente Técnico', NULL, 'Assistência Técnica', 'Chiaperini', NULL, NULL, '2023-11-29 19:27:57'),
        (9, '7270', NULL, 'Silverton (Tom)', 'Líder de Caldeiraria', NULL, 'Calderaria', 'Chiaperini', NULL, NULL, '2023-11-29 19:28:53'),
        (10, '7276', 'daiana@chiaperini.com.br', 'Daiana', 'Vendas de Equipamentos', NULL, 'Vendas', 'Chiaperini', NULL, NULL, '2024-09-26 14:51:59'),
        (11, '7288', 'comex@chiaperini.com.br', 'Marília', 'Comércio Exterior', NULL, 'Comércio Exterior', 'Chiaperini', 'comex.chiaperini', NULL, '2023-08-30 17:08:48'),
        (12, '7227', 'comex2@chiaperini.com.br', 'João Paulo', 'Comércio Exterior', NULL, 'Comércio Exterior', 'Chiaperini', NULL, NULL, '2025-07-29 19:14:04'),
        (13, '7388', 'comex1@chiaperini.com.br', 'Pedro Turatto', 'Comércio Exterior', NULL, 'Comércio Exterior', 'Chiaperini', 'live:.cid.3681860450356cfa', NULL, '2023-11-29 19:30:35'),
        (14, '7267', 'danilo@chiaperini.com.br', 'Danilo', 'Compras', NULL, 'Compras', 'Chiaperini', 'danilo.chiaperini', NULL, '2023-08-30 16:09:09'),
        (15, '7217', 'compras@chiaperini.com.br', 'Vera', 'Compradora', NULL, 'Compras', 'Chiaperini', 'vera.dorazio', NULL, '2023-11-29 19:31:31'),
        (16, '7250', 'compras2@chiaperini.com.br', 'Márcio Braga', 'comprador', NULL, 'Compras', 'Chiaperini', NULL, NULL, '2025-04-17 17:20:49'),
        (17, '7291', 'compras1@chiaperini.com.br', 'Elaine', 'Compradora', NULL, 'Compras', 'Chiaperini', 'elainer.chiaperini', NULL, '2023-11-29 19:31:51'),
        (18, '7349', 'pcp01@chiaperini.com.br', 'Mateus Pereira', 'PCP', NULL, 'Produção', 'Chiaperini', NULL, NULL, '2025-04-17 17:19:17'),
        (19, '7375', 'yuri@chiaperini.com.br', 'Yuri', 'Custos', NULL, 'Compras', 'Chiaperini', 'live:yuri.chiaperini', NULL, '2023-11-29 19:32:11'),
        (21, '7245', 'tadeu@chiaperini.com.br', 'Sr. Tadeu', 'Diretor', NULL, 'Diretoria', 'Chiaperini', NULL, NULL, '2023-08-30 17:04:27'),
        (22, '7244', 'engenharia@chiaperini.com.br', 'Rodrigo', 'Engenharia', NULL, 'Engenharia', 'Chiaperini', NULL, NULL, '2025-04-17 17:24:23'),
        (23, '7261', NULL, 'Wallace (fixo)', NULL, '', 'Engenharia', 'Chiaperini', NULL, NULL, NULL),
        (24, '7361', NULL, 'Wallace (móvel)', 'Qualidade', NULL, 'Engenharia', 'Chiaperini', NULL, NULL, '2023-11-29 19:36:49'),
        (25, '7265', 'engenharia03@chiaperini.com.br', 'Danilo Zaac', 'Engenharia', NULL, 'Engenharia', 'Chiaperini', 'live:.cid.7da7bcf726132524', NULL, '2023-08-30 16:04:48'),
        (26, '7219', 'caldeiraria01@chiaperini.com.br', 'Salomão', 'Qualidade', '16981181872', 'Qualidade', 'Chiaperini', NULL, NULL, '2025-06-05 21:48:00'),
        (27, '7365', NULL, 'Tiago', 'Engenharia', NULL, 'Engenharia', 'Chiaperini', NULL, NULL, '2023-11-29 19:35:43'),
        (28, '7364', NULL, 'Juninho Wiezel', 'Engenharia', NULL, 'Engenharia', 'Chiaperini', NULL, NULL, '2023-11-29 19:34:57'),
        (29, '7368', 'engenharia07@chiaperini.com.br', 'Adriano', 'Engenharia', NULL, 'Engenharia', 'Chiaperini', NULL, NULL, '2025-04-17 17:25:33'),
        (30, '7247', 'leandroferrari@chiaperini.com.br', 'Ferrari (Interno)', 'Expedição', NULL, 'Expedição', 'Chiaperini', 'live:.cid.8648ebad8900bf68', NULL, '2023-08-30 16:41:48'),
        (31, '7238', 'leandroferrari@chiaperini.com.br', 'Ferrari (Externo)', 'Expedição', NULL, 'Expedição', 'Chiaperini', NULL, NULL, '2025-04-17 17:17:24'),
        (32, '7282', 'eder@chiaperini.com.br', 'Eder', 'Faturista', NULL, 'Faturamento', 'Chiaperini', 'eder.chiaperini.faturamento', NULL, '2023-11-29 19:37:54'),
        (33, '7298', 'sandro@chiaperini.com.br', 'Sandro', 'Gerente de Controladoria', NULL, 'Financeiro', 'Chiaperini', 'sandroabaque', NULL, '2023-11-29 19:40:47'),
        (34, '7215', 'lais@chiaperini.com.br', 'Laís', 'Supervisora Financeira', NULL, 'Financeiro', 'Chiaperini', NULL, NULL, '2024-07-12 16:35:46'),
        (35, '7252', 'simone@chiaperini.com.br', 'Simone', 'Supervisora de Contabilidade', NULL, 'Contabilidade', 'Chiaperini', 'simone.chiaperini', NULL, '2023-12-05 19:50:27'),
        (36, '7251', 'loiraina@chiaperini.com.br', 'Loiraina', 'Financeiro', NULL, 'Financeiro', 'Chiaperini', 'live:leticiafinchiaperini', NULL, '2023-08-30 16:50:11'),
        (37, '7237', 'renata@chiaperini.com.br', 'Renata', 'Financeiro', NULL, 'Financeiro', 'Chiaperini', 'renata.chiaperini', NULL, '2023-08-30 17:16:53'),
        (39, '7289', 'luciana@chiaperini.com.br', 'Luciana', 'Financeiro', NULL, 'Financeiro', 'Chiaperini', 'live:luciana_3260', NULL, '2023-08-30 16:50:59'),
        (40, '7397', NULL, 'Tiago', 'Contabilidade', NULL, 'Contabilidade', 'Chiaperini', NULL, NULL, '2025-04-17 21:48:42'),
        (41, '7214', 'leticia@chiaperini.com.br', 'Letícia', 'Financeiro', NULL, 'Financeiro', 'Chiaperini', 'live:leticiafinchiaperini', NULL, '2023-08-30 16:49:21'),
        (42, '7362', NULL, 'Liliane', 'Contabilidade', NULL, 'Contabilidade', 'Chiaperini', NULL, NULL, '2023-12-05 19:50:47'),
        (43, '7338', 'financeiro01@chiaperini.com.br', 'Daniela Lebrão', 'Financeiro', NULL, 'Financeiro', 'Chiaperini', 'live:.cid.c3cb3fbbf8279b16', NULL, '2024-11-06 17:34:28'),
        (44, '7386', NULL, 'Celio', NULL, '', 'Ferramentaria', 'Chiaperini', NULL, NULL, NULL),
        (45, '7211', 'davi@chiaperini.com.br', 'Davi', 'Gestão de Produtos', NULL, 'Gestão de Produtos', 'Chiaperini', 'davi.chiaperini', NULL, '2023-08-30 16:13:50'),
        (46, '7399', 'produtos02@chiaperini.com.br', 'Fábio Kawamura', 'Produtos', NULL, 'Gestão de Produtos', 'Chiaperini', NULL, NULL, '2025-04-17 17:28:09'),
        (47, '7336', 'tatiana.rocha@chiaperini.com.br', 'Tatiana', 'Logística', NULL, 'Logística', 'Chiaperini', 'tatiana.chiaperini', NULL, '2025-04-28 15:25:59'),
        (48, '7228', 'logistica3@chiaperini.com.br', 'Carol Pereira', 'Logística', NULL, 'Logística', 'Chiaperini', 'live:.cid.2431880e7a11158a', NULL, '2023-08-30 16:11:41'),
        (49, '7277', 'laboratorio@chiaperini.com.br', 'Renan e Marcos do Vale', 'Engenharia', NULL, 'Laboratório', 'Chiaperini', NULL, NULL, '2025-04-17 21:42:50'),
        (50, '7222', 'manutencao@chiaperini.com.br', 'Lucas', 'Manutenção', NULL, 'Manutenção', 'Chiaperini', NULL, NULL, '2025-05-23 19:10:57'),
        (51, '7286', 'leonardo@chiaperini.com.br', 'Leonardo Gomes', 'Marketing', NULL, 'Marketing', 'Chiaperini', 'leonardo.chiaperini', NULL, '2023-08-30 16:47:17'),
        (52, '7311', NULL, 'Ricardo', 'Desenvolvimento de Produtos', NULL, 'Gestão de Produtos', 'Chiaperini', NULL, NULL, '2024-03-05 20:05:35'),
        (53, '7398', 'gregory@chiaperini.com.br', 'Grégory', 'Controladoria', NULL, 'Compras', 'Chiaperini', NULL, NULL, '2025-05-15 19:24:08'),
        (54, '7390', 'marketing2@chiaperini.com.br', 'Thaline', 'Marketing', NULL, 'Marketing', 'Chiaperini', NULL, NULL, '2025-04-17 19:48:14'),
        (55, '7389', 'marketing3@chiaperini.com.br', 'Murillo', 'Marketing', NULL, 'Marketing', 'Chiaperini', NULL, NULL, '2025-04-17 19:47:07'),
        (56, '7312', NULL, 'João Cunha', NULL, '', 'Marketing', 'Chiaperini', NULL, NULL, NULL),
        (57, '7313', 'marketing06@chiaperini.com.br', 'Luciel', 'Analista de E-commerce', NULL, 'Marketing', 'Chiaperini', 'https://join.skype.com/invite/htfLaaizllnw', NULL, '2024-04-17 17:17:55'),
        (58, '991531535', NULL, 'Marcio A', NULL, '991531535', 'Motoristas', 'Chiaperini', NULL, NULL, NULL),
        (59, '9915315351', NULL, 'Ederson', NULL, '992045533', 'Motoristas', 'Chiaperini', NULL, NULL, NULL),
        (60, '7259', NULL, 'Cristiano Lima', 'Montagem Final', NULL, 'Montagem Final', 'Chiaperini', NULL, NULL, '2023-11-29 19:47:35'),
        (61, '7248', 'teo@chiaperini.com.br', 'Téo', 'Produção', NULL, 'Produção', 'Chiaperini', 'teo.chiaperini', NULL, '2023-08-30 17:06:06'),
        (62, '7240', 'nacionalizados@chiaperini.com.br', 'Diego Mencucini', 'Nacionalizados', NULL, 'Nacionalizados', 'Chiaperini', 'live:.cid.e6ddb95e2d97f4c0', NULL, '2023-08-30 16:16:36'),
        (63, '7279', 'recepcaoat@chiaperini.com.br', 'Everaldo', 'Recepção Assistência', NULL, 'Assistência Técnica', 'Chiaperini', 'everaldo497', NULL, '2025-06-03 17:16:13'),
        (64, '7285', 'setor10@chiaperini.com.br', 'Lucas', 'Setor 10', NULL, 'Setor 10', 'Chiaperini', NULL, NULL, '2025-04-17 17:18:09'),
        (65, '7263', 'rh@chiaperini.com.br', 'Clovis', 'RH', NULL, 'RH', 'Chiaperini', 'clovis.chiaperini', NULL, '2023-08-30 15:55:05'),
        (66, '7212', 'silvia@chiaperini.com.br', 'Silvia', 'RH', NULL, 'RH', 'Chiaperini', 'silvia.martinelli37', NULL, '2023-08-30 17:35:17'),
        (67, '7234', 'rita@chiaperini.com.br', 'Rita', 'Técnica de Segurança', NULL, 'RH', 'Chiaperini', 'rita.chiaperini', NULL, '2023-08-30 17:17:52'),
        (68, '7366', NULL, 'Roberta', NULL, '', 'RH', 'Chiaperini', NULL, NULL, NULL),
        (71, '981659088', 'joseroberto@chiaperini.com.br', 'José Roberto', 'Gerente de Vendas', '981659088', 'Gerente de Vendas', 'Chiaperini', 'jrchiaperini', NULL, '2023-08-30 16:32:43'),
        (72, '991813275', NULL, 'Lucas', NULL, '991813275', 'Supervisores', 'Chiaperini', NULL, NULL, NULL),
        (73, '991895108', 'leonardogaspar@chiaperini.com.br', 'Leonardo Gaspar', 'Supervisor de Vendas', '991895108', 'Supervisores', 'Chiaperini', NULL, NULL, '2023-08-30 16:45:16'),
        (74, '993219147', 'luciano@chiaperini.com.br', 'Luciano Henrique', 'Supervisor de Vendas', '993219147', 'Supervisores', 'Chiaperini', NULL, NULL, '2023-08-30 16:54:39'),
        (75, '7266', 'fernanda@chiaperini.com.br', 'Fernanda', 'Supervisora de Vendas', '991095541', 'Vendas', 'Chiaperini', 'fernanda.chiaperini', NULL, '2025-02-06 21:56:45'),
        (76, '7010', 'kall.ti@chiaperini.com.br', 'Kall', 'T.I Infra', NULL, 'TI-Infra', 'Chiaperini', 'kallamalia', NULL, '2025-07-16 21:55:11'),
        (78, '7014', NULL, 'Lucas Coelho', 'Estagiário TI Infra', NULL, 'TI-Infra', 'Chiaperini', NULL, NULL, '2024-02-27 14:33:22'),
        (79, '7254', 'leonardo.ti@chiaperini.com.br', 'Leonardo TI-Infra', 'TI-Infra', NULL, 'TI-Infra', 'Chiaperini', NULL, NULL, '2025-08-07 15:43:24'),
        (80, '7333', 'jjcjunior@chiaperini.com.br', 'José Jorge', 'T.I Sistemas', NULL, 'TI-Sistemas', 'Chiaperini', 'josejorgecjunior', NULL, '2023-08-30 16:31:49'),
        (81, '7226', 'usinagem@chiaperini.com.br', 'Sandro', 'Usinagem', NULL, 'Usinagem', 'Chiaperini', NULL, NULL, '2025-06-16 16:16:37'),
        (82, '7379', 'alinem@chiaperini.com.br', 'Alinne', 'Vendas de Peças', NULL, 'Vendas de Peças', 'Chiaperini', 'alinem.chiaperini', NULL, '2025-04-17 17:33:36'),
        (83, '7348', 'cido@chiaperini.com.br', 'Cido', 'Vendas de Peças', NULL, 'Vendas de Peças', 'Chiaperini', NULL, NULL, '2025-04-17 17:36:17'),
        (84, '7391', 'caroline@chiaperini.com.br', 'Caroline Ribeiro', 'Vendas de Peças', NULL, 'Vendas de Peças', 'Chiaperini', 'caroline.chiaperini', NULL, '2025-04-17 17:30:06'),
        (85, '7082', 'jeancarlos@chiaperini.com.br', 'Jean', 'Vendas de Peças', NULL, 'Vendas de Peças', 'Chiaperini', NULL, NULL, '2025-04-17 17:34:52'),
        (87, '7232', 'roseli@chiaperini.com.br', 'Roseli', 'Gerente de Vendas', '993189484', 'Gerente de Vendas', 'Chiaperini', 'live:roseli_374', NULL, '2023-08-30 17:33:47'),
        (89, '7221', 'cecilia@chiaperini.com.br', 'Cecília', 'Vendas de Equipamentos', NULL, 'Vendas', 'Chiaperini', 'cecilia.chiaperini', NULL, '2023-08-30 16:00:39'),
        (90, '7231', 'rafaela@chiaperini.com.br', 'Rafaela', 'Vendas de Equipamentos', NULL, 'Vendas', 'Chiaperini', 'live:rafaela_46', NULL, '2023-08-30 17:16:06'),
        (91, '7230', 'kelly@chiaperini.com.br', 'Kelly', 'Vendas de Equipamentos', NULL, 'Vendas', 'Chiaperini', 'kelly.chiaperini', NULL, '2023-08-30 16:34:43'),
        (92, '7268', 'adriana@chiaperini.com.br', 'Adriana', 'Vendas Equipamentos', NULL, 'Vendas', 'Chiaperini', 'adrianac.chiaperini', NULL, '2023-08-30 15:42:59'),
        (93, '7216', NULL, 'Fabiana', 'Vendas de Equipamentos', NULL, 'Vendas', 'Chiaperini', NULL, NULL, '2024-04-16 16:33:05'),
        (94, '7287', 'marcia@chiaperini.com.br', 'Marcia', 'Vendas de Equipamentos', NULL, 'Vendas', 'Chiaperini', 'marcia.chiaperini', NULL, '2023-08-30 17:08:00'),
        (95, '7301', NULL, 'Marcos', NULL, '', 'Vendas', 'Chiaperini', NULL, NULL, NULL),
        (96, '7271', NULL, 'Mario', NULL, '', 'Vendas', 'Chiaperini', NULL, NULL, NULL),
        (97, '1639549420', NULL, 'Techto (Fixo)', NULL, '16 3954 9420', 'Techto', 'Techto', NULL, NULL, NULL),
        (98, '6002', 'roberval@techto.com.br', 'Roberval', 'Vendas', '992724866', 'Compressor Parafuso', 'Techto', NULL, NULL, '2025-04-17 17:48:29'),
        (99, '6001', 'roselaine@techto.com.br', 'Roselaine', 'Vendas', '992697298', 'Compressor Parafuso', 'Techto', NULL, NULL, '2025-04-17 17:47:53'),
        (100, '6005', 'agostinho.grilli@techto.com.br', 'Grilli', 'Vendas Compressor Parafuso', '993861728', 'Compressor Parafuso', 'Techto', NULL, NULL, '2025-04-17 19:28:56'),
        (101, '6013', 'vendas05@techto.com.br', 'Cosmo', 'Vendas', '991211857', 'Compressor Parafuso', 'Techto', NULL, NULL, '2025-04-17 17:46:16'),
        (102, '6006', NULL, 'Flávia', NULL, '', 'Compras', 'Techto', NULL, NULL, NULL),
        (103, '6004', NULL, 'Alfredo', NULL, '', 'Administrativo', 'Techto', NULL, NULL, NULL),
        (104, '6003', NULL, 'Maria Rita', NULL, '', 'Administrativo', 'Techto', NULL, NULL, NULL),
        (105, '6019', 'financeiro2@techto.com.br', 'Bianca Caroline', 'Auxiliar Administrativa', NULL, 'Financeiro', 'Techto', NULL, NULL, '2024-07-17 15:39:21'),
        (107, '6015', NULL, 'Ricardo Rangon', NULL, '', 'Gerente de Produção', 'Techto', NULL, NULL, NULL),
        (108, '6007', 'qualidade01@techto.com.br', 'Gabriella', 'Qualidade', NULL, 'Qualidade', 'Techto', NULL, NULL, '2025-04-17 17:42:13'),
        (109, '6017', 'qualidade02@techto.com.br', 'Luís Gustavo', 'qualidade', NULL, 'Qualidade', 'Techto', NULL, NULL, '2025-04-17 17:41:26'),
        (110, '6032', NULL, 'André', NULL, '', 'Manutenção', 'Techto', NULL, NULL, NULL),
        (111, '6014', NULL, 'Débora', NULL, '', 'Segurança do Trabalho', 'Techto', NULL, NULL, NULL),
        (112, '6038', NULL, 'Levi', NULL, '', 'Produção', 'Techto', NULL, NULL, NULL),
        (113, '6031', NULL, 'Montagem', NULL, '', 'Produção', 'Techto', NULL, NULL, NULL),
        (114, '6030', NULL, 'C. Parafuso', NULL, '', 'Produção', 'Techto', NULL, NULL, NULL),
        (115, '6036', NULL, 'Montagem Final', NULL, '', 'Produção', 'Techto', NULL, NULL, NULL),
        (116, '6033', NULL, 'Almoxarifado', NULL, '', 'Produção', 'Techto', NULL, NULL, NULL),
        (117, '6034', NULL, 'Plasma', NULL, '', 'Produção', 'Techto', NULL, NULL, NULL),
        (118, '6035', NULL, 'Pedro', 'Polímeros', NULL, 'Polímeros', 'Techto', NULL, NULL, '2023-12-05 19:49:45'),
        (119, '6039', NULL, 'Calderaria', NULL, '', 'Produção', 'Techto', NULL, NULL, NULL),
        (120, '6040', NULL, 'Cartonagem', NULL, '', 'Produção', 'Techto', NULL, NULL, NULL),
        (121, '1639549415', NULL, 'Mercadão Lojista (Fixo)', NULL, '', '1639549415', 'Mercadão Lojista', NULL, NULL, NULL),
        (122, '4003', 'compras02@mercadaolojista.com.br', 'Elton', 'compras', NULL, 'Compras', 'Mercadão Lojista', NULL, NULL, '2025-04-17 17:16:05'),
        (123, '4002', 'compras01@mercadaolojista.com.br', 'Mariane', 'Compras', NULL, 'Compras', 'Mercadão Lojista', NULL, NULL, '2025-04-17 17:15:29'),
        (124, '4004', 'compras03@mercadaolojista.com.br', 'Douglas', 'compras', NULL, 'Compras', 'Mercadão Lojista', NULL, NULL, '2025-04-17 17:16:29'),
        (125, '4010', 'financeiro@mercadaolojista.com.br', 'Mônica', 'Financeiro', NULL, 'Financeiro', 'Mercadão Lojista', NULL, NULL, '2025-04-17 19:42:30'),
        (126, '4011', 'financeiro02@mercadaolojista.com.br', 'Helaine', 'Financeiro', NULL, 'Financeiro', 'Mercadão Lojista', NULL, NULL, '2024-07-30 22:37:20'),
        (128, '7275', NULL, 'Luciano', NULL, '', 'Financeiro', 'Mercadão Lojista', NULL, NULL, NULL),
        (129, '4007', NULL, 'Elton', 'Expedição', NULL, 'Expedição', 'Mercadão Lojista', NULL, NULL, '2025-04-17 17:38:32'),
        (130, '4015', NULL, 'Ana', NULL, '', 'Vendas', 'Mercadão Lojista', NULL, NULL, NULL),
        (131, '4016', NULL, 'Verônica', 'Vendedora', NULL, 'Vendas', 'Mercadão Lojista', NULL, NULL, '2025-04-07 20:37:19'),
        (132, '4017', NULL, 'Guto', NULL, '', 'Vendas', 'Mercadão Lojista', NULL, NULL, NULL),
        (133, '1639549414', NULL, 'Chiaperini Pro (Fixo)', NULL, '', '1639549414', 'Chiaperini Pro', NULL, NULL, NULL),
        (134, '3003', NULL, 'Wagner', 'Supervisor de Vendas', NULL, 'Turma 01', 'Chiaperini Pro', NULL, NULL, '2023-11-29 16:34:31'),
        (137, '3015', 'chiaperinipro19@chiaperinipro.com.br', 'Jéssica', 'Operadora de Telemarketing', NULL, 'Turma 01', 'Chiaperini Pro', NULL, NULL, '2025-08-06 20:42:17'),
        (139, '3011', 'chiaperinipro10@chiaperinipro.com.br', 'Juliana', 'Op Telemarketing', NULL, 'Turma 01', 'Chiaperini Pro', NULL, NULL, '2025-04-17 16:46:50'),
        (140, '3012', 'chiaperinipro11@chiaperinipro.com.br', 'Vanessa', 'Operadora de Telemarketing', NULL, 'Turma 01', 'Chiaperini Pro', NULL, NULL, '2025-04-17 16:48:03'),
        (141, '3013', 'chiaperinipro12@chiaperinipro.com.br', 'Jaqueline', 'Operadora de Telemarketing', NULL, 'Turma 01', 'Chiaperini Pro', NULL, NULL, '2025-04-17 16:54:00'),
        (142, '4018', NULL, 'Maria Eduarda', 'Operadora de Telemarketing', NULL, 'turma 02 - 3DLA', 'Mercadão Lojista', NULL, NULL, '2023-11-27 20:20:47'),
        (143, '4019', NULL, 'Ana Carolina', 'Operadora de Telemarketing', NULL, 'turma 02 - 3DLA', 'Mercadão Lojista', NULL, NULL, '2024-01-15 15:24:45'),
        (144, '3017', 'chiaperinipro15@chiaperinipro.com.br', 'Priscila', 'Operadora de Telemarketing', NULL, 'Turma 01', 'Chiaperini Pro', NULL, NULL, '2025-04-17 17:12:46'),
        (145, '3018', 'chiaperinipro21@chiaperinipro.com.br', 'Tamires', 'Operadora de Telemarketing', NULL, 'Turma 03', 'Chiaperini Pro', NULL, NULL, '2025-04-17 17:13:27'),
        (150, '3023', 'chiaperinipro08@chiaperinipro.com.br', 'Ana Lívia', 'Op Telemarketing', NULL, 'Turma 03', 'Chiaperini Pro', NULL, NULL, '2025-04-17 16:43:44'),
        (151, '3006', 'chiaperinipro05@chiaperinipro.com.br', 'Ana Laura', 'Operadora de Telemarketing', NULL, 'Turma 03', 'Chiaperini Pro', NULL, NULL, '2025-04-17 16:43:15'),
        (153, '1639549416', NULL, 'FNC (Fixo)', NULL, '', 'FNC', 'FNC', NULL, NULL, NULL),
        (154, '5001', NULL, 'Antônio', 'Gerente FNC', NULL, 'Gerência', 'FNC', NULL, NULL, '2023-12-05 18:05:13'),
        (155, '5002', 'fundicao01@fundicaonatividade.com.br', 'Felipe', 'Laboratório', NULL, 'FNC', 'FNC', NULL, NULL, '2025-04-17 17:37:22'),
        (157, '7339', 'financeiro06@chiaperini.com.br', 'Jaqueline', 'Financeiro', NULL, 'Financeiro', 'Chiaperini', NULL, '2023-08-17 15:32:43', '2025-04-17 21:39:49'),
        (159, '7086', NULL, 'Júlia', 'Logística', NULL, 'Logística', 'Chiaperini', NULL, '2023-08-17 15:35:12', '2025-04-24 14:47:32'),
        (160, '7363', NULL, 'Victor', 'Engenharia', NULL, 'Engenharia', 'Chiaperini', NULL, '2023-08-17 15:36:47', '2023-11-29 19:36:27'),
        (161, '7345', 'vendas.pecas01@chiaperini.com.br', 'Larissa', 'Vendas de Peças', NULL, 'Vendas de Peças', 'Chiaperini', NULL, '2023-08-17 15:37:34', '2025-04-17 17:32:46'),
        (162, '7015', NULL, 'Iuri', 'TI', NULL, 'TI-Sistemas', 'Chiaperini', NULL, '2023-08-23 19:03:46', '2024-07-17 14:39:36'),
        (163, '6043', 'vendas02@techto.com.br', 'Murilo', 'Analista de Vendas', NULL, 'Vendas', 'Techto', NULL, '2023-09-27 17:56:10', '2025-04-17 17:49:00'),
        (164, '7324', 'lucasferreira@chiaperini.com.br', 'Lucas Ferreira', 'Estagiário', NULL, 'Faturamento', 'Chiaperini', NULL, '2023-10-09 14:40:48', '2023-10-09 14:40:48'),
        (166, '7369', NULL, 'Fabrício', 'Engenharia', NULL, 'Engenharia', 'Chiaperini', NULL, '2023-11-24 20:52:50', '2023-11-24 20:52:50'),
        (167, '7371', NULL, 'Felipe', 'Analista de Processos', NULL, 'Engenharia', 'Chiaperini', NULL, '2023-11-24 20:53:47', '2023-11-24 20:53:47'),
        (168, '7280', NULL, 'Ivanilson', 'Expedição CDNE', NULL, 'Expedição', 'Chiaperini', NULL, '2023-11-24 20:54:52', '2023-11-29 19:33:57'),
        (169, '6050', NULL, 'Maria Eduarda', 'Compras', NULL, 'Compras', 'Techto', NULL, '2023-11-24 20:56:28', '2024-07-03 19:17:53'),
        (170, '6012', NULL, 'Thiago', 'Estagiário', NULL, 'Segurança do Trabalho', 'Techto', NULL, '2023-11-24 20:57:07', '2023-11-24 20:57:07'),
        (172, '3002', 'chiaperinipro02@chiaperinipro.com.br', 'Vitória', 'Operadora de Telemarketing', NULL, 'Turma 01', 'Chiaperini Pro', NULL, '2023-11-24 20:59:05', '2025-08-06 20:43:11'),
        (177, '6041', 'vendas01@techto.com.br', 'Valéria', 'Vendas', NULL, 'Vendas', 'Techto', NULL, '2023-11-24 21:07:38', '2025-04-17 17:47:03'),
        (178, '7328', NULL, 'Really', 'Faturamento', NULL, 'Faturamento', 'Chiaperini', NULL, '2023-11-24 21:10:34', '2024-06-17 22:29:53'),
        (179, '4022', NULL, 'Beatriz', 'Operadora de Telemarketing', NULL, 'Turma 02', 'Mercadão Lojista', NULL, '2023-11-27 20:14:53', '2023-11-27 20:21:26'),
        (180, '4020', NULL, 'Kauane', 'Operadora de Telemarketing', NULL, 'Turma 02', 'Mercadão Lojista', NULL, '2023-11-28 17:47:40', '2023-11-28 17:47:40'),
        (181, '6011', NULL, 'Rafhael', 'Analista de TI', NULL, 'TI-Sistemas', 'Techto', NULL, '2023-12-05 18:00:23', '2024-10-03 19:21:06'),
        (182, '6042', NULL, 'Lucas Martins', 'CNC', NULL, 'CNC', 'Techto', NULL, '2023-12-05 18:01:09', '2023-12-05 19:49:18'),
        (183, '6008', NULL, 'Marcelo', 'Financeiro', NULL, 'Financeiro', 'Techto', NULL, '2023-12-05 18:03:53', '2023-12-05 18:03:53'),
        (184, '7253', NULL, 'Ane', 'Contabilidade', NULL, 'Contabilidade', 'Chiaperini', NULL, '2023-12-05 18:06:40', '2023-12-05 19:50:06'),
        (185, '7314', NULL, 'Gabriel 3DLA', 'Estágiário', NULL, 'Marketing', 'Mercadão Lojista', NULL, '2024-02-02 17:48:29', '2024-02-02 17:48:29'),
        (186, '7302', NULL, 'Claudevir', 'Comercial', NULL, 'Vendas', 'Chiaperini', NULL, '2024-03-06 15:09:18', '2024-03-06 15:09:18'),
        (187, '7273', NULL, 'Tainne', 'Vendas', NULL, 'Vendas', 'Chiaperini', NULL, '2024-04-01 17:48:09', '2024-04-01 17:48:09'),
        (188, '7315', 'merketing09@chiaperini.com.br', 'Felipe Gerardi', 'Analista de E-Commerce', NULL, 'Marketing', 'Chiaperini', NULL, '2024-04-02 17:32:19', '2024-04-02 17:32:19'),
        (189, '7392', 'vendas.pecas03@chiaperini.com.br', 'Maria Eduarda', 'Vendas de Peças', NULL, 'Vendas de Peças', 'Chiaperini', NULL, '2024-04-03 15:10:39', '2025-06-10 20:53:40'),
        (190, '7393', 'vendas.pecas04@chiaperini.com.br', 'Naiara Orlando', 'Vendas de Peças', NULL, 'Vendas de Peças', 'Chiaperini', NULL, '2024-04-03 15:11:07', '2025-04-17 17:31:45'),
        (191, '7316', 'marketing10@chiaperini.com.br', 'Brenda', 'Aux Mkt', NULL, 'Marketing', 'Chiaperini', NULL, '2024-04-11 17:04:58', '2025-04-17 19:49:09'),
        (192, '7394', 'marketing4@chiaperini.com.br', 'Gabriel Carvalho', 'MKT', NULL, 'Marketing', 'Chiaperini', NULL, '2024-04-11 17:05:31', '2025-04-17 19:49:55'),
        (193, '3020', 'chiaperinipro22@chiaperinipro.com.br', 'Thamiris', 'Operadora de Telemarketing', NULL, 'Turma 03', 'Chiaperini Pro', NULL, '2024-04-15 20:53:18', '2025-04-17 16:42:42'),
        (196, '6045', 'vendas04@techto.com.br', 'Marinela', 'Vendas', NULL, 'Vendas', 'Techto', NULL, '2024-05-13 14:11:44', '2025-01-20 15:16:32'),
        (197, '6056', 'cortecnc1@techto.com.br', 'Keila e Fernanda', 'Corte de Juntas', NULL, 'CNC', 'Techto', NULL, '2024-06-11 16:46:55', '2025-04-17 17:23:19'),
        (198, '6018', 'qualidade03@techto.com.br', 'Yeda', 'Estagiária Qualidade', NULL, 'Qualidade', 'Techto', NULL, '2024-06-18 15:01:07', '2025-02-12 16:21:21'),
        (199, '6060', NULL, 'Igor', 'Expedição', NULL, 'Expedição', 'Techto', NULL, '2024-07-03 19:17:02', '2024-07-16 15:54:06'),
        (200, '7017', NULL, 'Isa', 'Estagiária', NULL, 'TI-Sistemas', 'Chiaperini', NULL, '2024-07-17 14:37:12', '2024-07-17 14:37:12'),
        (201, '7016', NULL, 'Guilherme', 'TI', NULL, 'TI-Sistemas', 'Chiaperini', NULL, '2024-07-17 14:39:58', '2024-07-17 14:39:58'),
        (202, '7012', NULL, 'Gabriel', 'TI', NULL, 'TI-Sistemas', 'Chiaperini', NULL, '2024-07-17 14:40:23', '2024-07-17 14:40:23'),
        (203, '6048', 'rh02@techto.com.br', 'RH Techto', 'RH', NULL, 'RH', 'Techto', NULL, '2024-08-06 19:51:50', '2025-02-28 17:04:21'),
        (204, '7396', 'vendas.pecas06@chiaperini.com.br', 'Marcela', 'Vendas de Peças', NULL, 'Vendas de Peças', 'Chiaperini', NULL, '2024-08-16 14:56:51', '2025-02-18 14:59:30'),
        (205, '7395', 'vendas.pecas05@chiaperini.com.br', 'Ísis', 'Vendas de Peças', NULL, 'Vendas de Peças', 'Chiaperini', NULL, '2024-08-16 14:57:23', '2024-08-16 14:57:23'),
        (206, '7274', 'daniely@chiaperini.com.br', 'Daniely', 'Vendas de Equipamentos', NULL, 'Vendas', 'Chiaperini', NULL, '2024-09-26 14:50:35', '2024-09-26 14:50:35'),
        (207, '7370', 'caldeiraria@chiaperini.com.br', 'Carlos', 'Caldeiraria/ Qualidade', '16981181872', 'Qualidade', 'Chiaperini', NULL, '2024-10-28 14:26:09', '2025-06-05 21:40:13'),
        (210, '3010', 'chiaperinipro18@chiaperinipro.com.br', 'Naiara Martins', 'Operadora de Telemarketing', NULL, 'Vendas', 'Chiaperini Pro', NULL, '2024-10-28 16:47:29', '2025-04-17 17:07:37'),
        (211, '3014', 'chiaperinipro20@chiaperinipro.com.br', 'Anna Lívia Izidoro', 'Operadora de Telemarketing', NULL, 'Vendas', 'Chiaperini Pro', NULL, '2024-10-28 16:47:58', '2025-04-17 17:18:34'),
        (212, '3021', NULL, 'Verônica', 'Operadora de Telemarketing', NULL, 'Vendas', 'Chiaperini Pro', NULL, '2024-10-28 16:50:01', '2024-10-28 16:50:01'),
        (213, '3022', 'chiaperinipro24@chiaperinipro.com.br', 'Amanda', 'Operadora de Telemarketing', NULL, 'Vendas', 'Chiaperini Pro', NULL, '2024-10-28 16:50:30', '2025-04-17 16:41:57'),
        (215, '6020', NULL, 'Isabelly', 'Financeiro', NULL, 'Financeiro', 'Techto', NULL, '2024-11-05 18:01:08', '2025-05-23 17:24:39'),
        (216, '7278', NULL, 'Léia', 'Vendas', NULL, 'Vendas', 'Chiaperini', NULL, '2025-01-17 20:40:48', '2025-01-17 20:40:48'),
        (218, '7218', 'financeiro04@chiaperini.com.br', 'Andresa', 'Financeiro', NULL, 'Financeiro', 'Chiaperini', NULL, '2025-02-11 15:35:36', '2025-02-11 15:35:36'),
        (219, '7372', NULL, 'Willians', 'Engenharia de Processo', NULL, 'Engenharia', 'Chiaperini', NULL, '2025-02-26 15:10:39', '2025-02-26 15:10:39'),
        (220, '6044', 'vendas03@techto.com.br', 'Patricia', 'Vendas', NULL, 'Vendas', 'Techto', NULL, '2025-03-06 21:31:11', '2025-04-17 17:49:38'),
        (221, '4005', NULL, 'Elton', 'Expedição', NULL, 'Expedição', 'Mercadão Lojista', NULL, '2025-04-17 19:59:38', '2025-04-17 19:59:38'),
        (223, '7030', 'fabrica@techto.com.br', 'Gean', 'Fabrica', NULL, 'Produção', 'Techto', NULL, '2025-04-17 20:05:00', '2025-04-17 20:05:00'),
        (224, '6046', 'vendas05@techto.com.br', 'Mariana', 'Vendas', NULL, 'Vendas', 'Techto', NULL, '2025-04-17 20:05:58', '2025-04-17 20:05:58'),
        (225, '4013', 'faturamento@mercadaolojista.com.br', 'Solange', 'Faturamento', NULL, 'Faturamento', 'Mercadão Lojista', NULL, '2025-04-17 20:06:49', '2025-04-17 20:06:49'),
        (226, '7235', 'financeiro05@chiaperini.com.br', 'Carina', 'Financeiro', NULL, 'Financeiro', 'Chiaperini', NULL, '2025-04-17 20:14:09', '2025-04-17 20:14:09'),
        (227, '6016', NULL, 'Ana Carolina Chitero', 'Financeiro', NULL, 'Financeiro', 'Techto', NULL, '2025-04-25 17:11:23', '2025-04-25 17:11:23'),
        (228, '7210', NULL, 'Sabrina - Recepção', 'Telefonista', NULL, 'Administrativo', 'Chiaperini', NULL, '2025-05-07 19:13:31', '2025-05-23 19:49:52'),
        (229, '7224', NULL, 'Cauã', 'Qualidade', '16981181872', 'Qualidade', 'Chiaperini', NULL, '2025-05-12 15:07:56', '2025-06-05 21:48:31'),
        (230, '7264', NULL, 'Portaria', 'Porteiro', NULL, 'Administrativo', 'Chiaperini', NULL, '2025-05-15 22:18:14', '2025-05-15 22:18:14'),
        (231, '7346', NULL, 'Andreza', 'Assistente Técnica', NULL, 'Assistência Técnica', 'Chiaperini', NULL, '2025-06-09 14:31:36', '2025-06-09 14:31:36'),
        (232, '7236', NULL, 'Wendel', 'RH', NULL, 'RH', 'Chiaperini', NULL, '2025-06-26 16:41:51', '2025-06-26 16:41:51'),
        (233, '7088', NULL, 'Airton', 'Logistica', NULL, 'Logística', 'Chiaperini', NULL, '2025-06-27 16:08:53', '2025-07-16 20:38:55'),
        (234, '3005', 'chiaperinipro04@chiaperinipro.com.br', 'Paola', 'Operadora de Telemarketing', NULL, 'Vendas', 'Chiaperini Pro', NULL, '2025-08-06 20:46:36', '2025-08-06 20:48:23'),
        (235, '3007', 'chiaperinipro16@chiaperinipro.com.br', 'Mel', 'Operadora de Telemarketing', NULL, 'Vendas', 'Chiaperini Pro', NULL, '2025-08-06 20:49:47', '2025-08-06 20:49:47'),
        (236, '3009', 'chiaperinipro07@chiaperinipro.com.br', 'Gislaine', 'Operadora de Telemarketing', NULL, 'Vendas', 'Chiaperini Pro', NULL, '2025-08-06 20:51:37', '2025-08-06 20:51:37'),
        (237, '3019', 'chiaperinipro19@chiaperinipro.com.br', 'Jéssica Pró', 'Operadora de Telemarketing', NULL, 'Vendas', 'Chiaperini Pro', NULL, '2025-08-06 20:52:31', '2025-08-06 20:52:31'),
        (238, '3016', 'chiaperinipro14@chiaperinipro.com.br', 'Emilly', 'Operadora de Telemarketing', NULL, 'Vendas', 'Chiaperini Pro', NULL, '2025-08-06 20:53:20', '2025-08-06 20:53:20'),
        (239, '4021', NULL, 'Maria Eduarda', 'Vendas 3DLA', NULL, 'Vendas', 'Mercadão Lojista', NULL, '2025-08-06 21:20:00', '2025-08-06 21:20:00'),
        (240, '4023', NULL, 'Ana Caroline', 'Vendas 3DLA', NULL, 'Vendas', 'Mercadão Lojista', NULL, '2025-08-06 21:20:42', '2025-08-06 21:20:42'),
        (241, '7249', NULL, 'Luis Henrique (Barracão Verde)', 'Expedição', NULL, 'Expedição', 'Techto', NULL, '2025-08-06 22:03:32', '2025-08-07 17:53:38'),
        (242, '7233', NULL, 'Roberto - Supermercado Peças', 'Supermercado Peças', NULL, 'Supermercado de peças', 'Chiaperini', NULL, '2025-08-11 22:31:05', '2025-08-11 22:31:05');"""
        
        return self._parse_sql_inserts(sql_data)

    def _parse_sql_inserts(self, sql_data):
        """Converte os INSERTs SQL em dados Python automaticamente"""
        pessoas = []
        
        # Regex para extrair os VALUES
        pattern = r'\((\d+),\s*\'([^\']*)\',\s*(?:\'([^\']*)\'\s*|NULL),\s*\'([^\']*)\',\s*(?:\'([^\']*)\'\s*|NULL),\s*(?:\'([^\']*)\'\s*|NULL),\s*\'([^\']*)\',\s*\'([^\']*)\',\s*(?:\'([^\']*)\'\s*|NULL)'
        
        matches = re.findall(pattern, sql_data)
        
        for match in matches:
            pessoa = {
                'Ramal': match[1] if match[1] else None,
                'Email': match[2] if match[2] and match[2] != 'NULL' else None,
                'Nome': self._clean_encoding(match[3]),
                'Funcao': self._clean_encoding(match[4]) if match[4] else None,
                'Whatsapp': match[5] if match[5] else None,
                'Departamento': self._clean_encoding(match[6]),
                'Unidade': match[7],
                'Teams': match[8] if match[8] else None,  # Skype vira Teams
            }
            pessoas.append(pessoa)
        
        return pessoas

    def _clean_encoding(self, text):
        """Limpa problemas de encoding"""
        if not text:
            return None
        
        replacements = {
            'Ã¡': 'á', 'Ã£': 'ã', 'Ã§': 'ç', 'Ã©': 'é', 'Ã­': 'í', 
            'Ã³': 'ó', 'Ãº': 'ú', 'Ã ': 'à', 'Ãª': 'ê', 'Ã´': 'ô'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text

    def _import_data(self, dados_pessoas):
        """Importa os dados para o banco"""
        contador_criados = 0
        contador_atualizados = 0
        
        for pessoa_data in dados_pessoas:
            # Criar/obter departamento
            departamento = None
            if pessoa_data['Departamento']:
                departamento, created = Departamento.objects.get_or_create(
                    nome=pessoa_data['Departamento'],
                    defaults={'ativo': True}
                )
            
            # Criar/obter função
            funcao = None
            if pessoa_data['Funcao']:
                funcao, created = Funcao.objects.get_or_create(
                    nome=pessoa_data['Funcao'],
                    defaults={'ativo': True}
                )
            
            # Criar/obter unidade
            unidade = None
            if pessoa_data['Unidade']:
                unidade, created = Unidade.objects.get_or_create(
                    nome=pessoa_data['Unidade'],
                    defaults={'ativo': True}
                )
            
            # Criar/atualizar funcionário
            funcionario, created = Funcionario.objects.update_or_create(
                nome=pessoa_data['Nome'],
                defaults={
                    'ramal': pessoa_data['Ramal'],
                    'email': pessoa_data['Email'],
                    'whatsapp': pessoa_data['Whatsapp'],
                    'teams': pessoa_data['Teams'],
                    'departamento': departamento,
                    'funcao': funcao,
                    'unidade': unidade,
                    'ativo': True
                }
            )
            
            if created:
                contador_criados += 1
            else:
                contador_atualizados += 1
        
        self.stdout.write(f'Funcionários criados: {contador_criados}')
        self.stdout.write(f'Funcionários atualizados: {contador_atualizados}')