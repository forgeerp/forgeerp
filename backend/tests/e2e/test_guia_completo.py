"""
Testes que geram guia passo a passo completo do ForgeERP.

Para gerar documentação, execute:
    pytest tests/e2e/test_guia_completo.py --generate-docs -v

Ou use o Makefile:
    make docs-e2e
"""

import pytest
from pathlib import Path
from datetime import datetime
from playwright.sync_api import Page
import time

from tests.e2e.utils import wait_for_react, wait_for_navigation_complete


@pytest.fixture
def docs_output_dir(request):
    """Output directory for generated documentation"""
    output_dir = Path("docs/operacional/screenshots")
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


@pytest.fixture
def should_generate_docs(request):
    """Check if documentation should be generated"""
    return request.config.getoption("--generate-docs")


class GuiaCompleto:
    """Helper class to generate complete step-by-step guide"""
    
    def __init__(self, page: Page, output_dir: Path):
        self.page = page
        self.output_dir = output_dir
        self.steps = []
        self.step_number = 1
    
    def add_step(self, title: str, instructions: list, screenshot_name: str):
        """Add a documentation step"""
        screenshot_path = self.output_dir / f"{screenshot_name}.png"
        self.page.screenshot(path=str(screenshot_path), full_page=True)
        
        step = {
            "step": self.step_number,
            "title": title,
            "instructions": instructions,
            "screenshot": f"operacional/screenshots/{screenshot_name}.png",
            "screenshot_name": screenshot_name
        }
        
        self.steps.append(step)
        self.step_number += 1
        return step
    
    def generate_markdown(self, filename: str = "GUIA_PASSO_A_PASSO.md"):
        """Generate step-by-step markdown documentation"""
        md_path = self.output_dir.parent / filename
        md_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# 📖 Guia Passo a Passo - ForgeERP\n\n")
            f.write(f"Este guia foi gerado automaticamente pelos testes E2E.\n\n")
            f.write(f"**Gerado em:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            f.write("## 📋 Índice\n\n")
            for step in self.steps:
                f.write(f"{step['step']}. [{step['title']}](#passo-{step['step']}-{step['title'].lower().replace(' ', '-').replace(':', '')})\n")
            f.write("\n---\n\n")
            
            for step in self.steps:
                f.write(f"## Passo {step['step']}: {step['title']}\n\n")
                f.write(f"![{step['screenshot_name']}]({step['screenshot']})\n\n")
                
                f.write("### O que fazer:\n\n")
                for i, instruction in enumerate(step['instructions'], 1):
                    f.write(f"{i}. {instruction}\n")
                
                f.write("\n---\n\n")
        
        print(f"✅ Guia gerado em: {md_path}")


def test_guia_completo(
    page: Page, 
    docs_output_dir: Path, 
    should_generate_docs: bool, 
    frontend_url: str, 
    api_url: str
):
    """Teste completo que gera guia passo a passo de todas as funcionalidades"""
    if not should_generate_docs:
        pytest.skip("Execute com --generate-docs para gerar documentação")
    
    guia = GuiaCompleto(page, docs_output_dir)
    
    # ============================================
    # PASSO 1: Acessar a aplicação
    # ============================================
    page.goto(frontend_url, wait_until="networkidle", timeout=30000)
    wait_for_react(page)
    time.sleep(2)  # Esperar renderização completa
    
    guia.add_step(
        "Acessar a aplicação",
        [
            f"Abra o navegador e acesse: {frontend_url}",
            "A página de login será exibida automaticamente",
            "Você verá o formulário de login com campos para usuário e senha"
        ],
        "01_acessar_aplicacao"
    )
    
    # ============================================
    # PASSO 2: Fazer login
    # ============================================
    # Preencher usuário
    username_selectors = [
        'input[id="username"]',
        'input[type="text"]',
        'input[placeholder*="admin"]',
    ]
    for selector in username_selectors:
        try:
            input_field = page.locator(selector).first
            if input_field.count() > 0:
                input_field.fill("admin")
                break
        except:
            continue
    
    time.sleep(1)
    guia.add_step(
        "Preencher campo de usuário",
        [
            "No campo 'Usuário', digite: **admin**",
            "Este é o usuário padrão do sistema",
            "O campo aceita apenas texto"
        ],
        "02_preencher_usuario"
    )
    
    # Preencher senha
    try:
        password_input = page.locator('input[type="password"]').first
        if password_input.count() > 0:
            password_input.fill("admin")
    except Exception as e:
        print(f"⚠️  Não foi possível preencher senha: {e}")
    
    time.sleep(1)
    guia.add_step(
        "Preencher campo de senha",
        [
            "No campo 'Senha', digite: **admin**",
            "Esta é a senha padrão do sistema",
            "A senha é ocultada por segurança (aparece como ••••••••)"
        ],
        "03_preencher_senha"
    )
    
    # Clicar em entrar
    submit_selectors = [
        'button[type="submit"]',
        'button:has-text("Entrar")',
        'button:has-text("Login")',
    ]
    for selector in submit_selectors:
        try:
            button = page.locator(selector).first
            if button.count() > 0:
                button.click()
                time.sleep(3)
                wait_for_navigation_complete(page)
                break
        except:
            continue
    
    guia.add_step(
        "Clicar em 'Entrar'",
        [
            "Clique no botão **'Entrar'**",
            "O sistema irá validar suas credenciais",
            "Se corretas, você será redirecionado para o dashboard"
        ],
        "04_login_sucesso"
    )
    
    # ============================================
    # PASSO 5: Dashboard
    # ============================================
    time.sleep(2)  # Esperar dashboard carregar
    wait_for_react(page)
    
    guia.add_step(
        "Visualizar Dashboard",
        [
            "Após fazer login, você verá o **Dashboard**",
            "No topo, há um menu de navegação com: Dashboard, Clientes, Configurações",
            "No centro, você verá estatísticas e uma lista de clientes recentes"
        ],
        "05_dashboard"
    )
    
    # ============================================
    # PASSO 6: Navegar para Clientes
    # ============================================
    try:
        # Tentar encontrar link de Clientes
        client_links = [
            'a[href="/clients"]',
            'text=Clientes',
            'button:has-text("Clientes")',
        ]
        for selector in client_links:
            try:
                element = page.locator(selector).first
                if element.count() > 0:
                    element.click()
                    wait_for_navigation_complete(page)
                    break
            except:
                continue
        
        time.sleep(2)
        wait_for_react(page)
        
        guia.add_step(
            "Navegar para página de Clientes",
            [
                "Clique na aba **'Clientes'** no menu superior",
                "Você será redirecionado para a página de gerenciamento de clientes",
                "Aqui você pode criar, editar e excluir clientes"
            ],
            "06_pagina_clientes"
        )
    except Exception as e:
        print(f"⚠️  Não foi possível navegar para Clientes: {e}")
    
    # ============================================
    # PASSO 7: Criar novo cliente
    # ============================================
    try:
        # Procurar botão "Novo Cliente" ou "+"
        create_buttons = [
            'button:has-text("Novo Cliente")',
            'button:has-text("+ Novo Cliente")',
            'button:has-text("+")',
        ]
        for selector in create_buttons:
            try:
                button = page.locator(selector).first
                if button.count() > 0:
                    button.click()
                    time.sleep(1)
                    wait_for_react(page)
                    break
            except:
                continue
        
        time.sleep(1)
        
        guia.add_step(
            "Clicar em 'Novo Cliente'",
            [
                "Clique no botão **'+ Novo Cliente'** no topo da página",
                "Um formulário será exibido para criar um novo cliente"
            ],
            "07_formulario_criar_cliente"
        )
        
        # Preencher formulário
        try:
            # Nome
            name_inputs = [
                'input[placeholder*="Nome"]',
                'input[type="text"]',
            ]
            for selector in name_inputs:
                try:
                    input_field = page.locator(selector).first
                    if input_field.count() > 0:
                        input_field.fill("Cliente Exemplo")
                        break
                except:
                    continue
            
            time.sleep(0.5)
            
            # Código
            code_inputs = [
                'input[placeholder*="código"]',
                'input[placeholder*="code"]',
            ]
            for selector in code_inputs:
                try:
                    input_field = page.locator(selector).first
                    if input_field.count() > 0:
                        input_field.fill("cliente-exemplo")
                        break
                except:
                    continue
            
            time.sleep(0.5)
            
            guia.add_step(
                "Preencher dados do cliente",
                [
                    "No campo **'Nome'**, digite: Cliente Exemplo",
                    "No campo **'Código'**, digite: cliente-exemplo",
                    "O código deve ser único e não pode ser alterado após criação",
                    "Preencha também Email, Domínio e Prefixo do Namespace (opcionais)"
                ],
                "08_preencher_dados_cliente"
            )
            
            # Clicar em criar
            submit_buttons = [
                'button:has-text("Criar")',
                'button[type="submit"]',
            ]
            for selector in submit_buttons:
                try:
                    button = page.locator(selector).first
                    if button.count() > 0:
                        button.click()
                        time.sleep(2)
                        wait_for_navigation_complete(page)
                        break
                except:
                    continue
            
            time.sleep(2)
            wait_for_react(page)
            
            guia.add_step(
                "Salvar cliente",
                [
                    "Clique no botão **'Criar'**",
                    "O cliente será salvo no banco de dados",
                    "Você será redirecionado para a lista de clientes"
                ],
                "09_cliente_criado"
            )
        except Exception as e:
            print(f"⚠️  Não foi possível preencher formulário: {e}")
    except Exception as e:
        print(f"⚠️  Não foi possível criar cliente: {e}")
    
    # ============================================
    # PASSO 10: Listar clientes
    # ============================================
    time.sleep(2)
    wait_for_react(page)
    
    guia.add_step(
        "Visualizar lista de clientes",
        [
            "Na página de Clientes, você verá uma tabela com todos os clientes cadastrados",
            "A tabela mostra: Nome, Código, Email, Domínio, Status e Ações",
            "Você pode editar ou excluir clientes clicando nos botões correspondentes"
        ],
        "10_lista_clientes"
    )
    
    # ============================================
    # PASSO 11: Editar cliente
    # ============================================
    try:
        # Procurar botão "Editar"
        edit_buttons = [
            'button:has-text("Editar")',
            'a:has-text("Editar")',
        ]
        for selector in edit_buttons:
            try:
                button = page.locator(selector).first
                if button.count() > 0:
                    button.click()
                    time.sleep(2)
                    wait_for_react(page)
                    break
            except:
                continue
        
        time.sleep(1)
        
        guia.add_step(
            "Editar cliente",
            [
                "Clique no botão **'Editar'** na linha do cliente desejado",
                "O formulário será preenchido com os dados do cliente",
                "Você pode modificar os campos (exceto o código)",
                "Clique em **'Atualizar'** para salvar as alterações"
            ],
            "11_editar_cliente"
        )
    except Exception as e:
        print(f"⚠️  Não foi possível editar cliente: {e}")
    
    # ============================================
    # PASSO 12: Navegar para Configurações
    # ============================================
    try:
        config_links = [
            'a[href="/configurations"]',
            'text=Configurações',
            'button:has-text("Configurações")',
        ]
        for selector in config_links:
            try:
                element = page.locator(selector).first
                if element.count() > 0:
                    element.click()
                    wait_for_navigation_complete(page)
                    break
            except:
                continue
        
        time.sleep(2)
        wait_for_react(page)
        
        guia.add_step(
            "Navegar para Configurações",
            [
                "Clique na aba **'Configurações'** no menu superior",
                "Você será redirecionado para a página de configurações",
                "Aqui você pode gerenciar configurações globais do sistema"
            ],
            "12_pagina_configuracoes"
        )
    except Exception as e:
        print(f"⚠️  Não foi possível navegar para Configurações: {e}")
    
    # ============================================
    # PASSO 13: Logout
    # ============================================
    try:
        logout_buttons = [
            'button:has-text("Sair")',
            'text=Sair',
        ]
        for selector in logout_buttons:
            try:
                button = page.locator(selector).first
                if button.count() > 0:
                    button.click()
                    time.sleep(2)
                    wait_for_navigation_complete(page)
                    break
            except:
                continue
        
        time.sleep(1)
        wait_for_react(page)
        
        guia.add_step(
            "Fazer logout",
            [
                "Clique no botão **'Sair'** no canto superior direito",
                "Você será deslogado e redirecionado para a página de login",
                "Para acessar novamente, você precisará fazer login novamente"
            ],
            "13_logout"
        )
    except Exception as e:
        print(f"⚠️  Não foi possível fazer logout: {e}")
    
    # Gerar documentação final
    guia.generate_markdown()
    
    print(f"\n✅ Guia completo gerado com {len(guia.steps)} passos!")

