"""
Testes que geram documentação visual automaticamente.

Para gerar documentação, execute:
    pytest tests/e2e/test_documentation.py --generate-docs

Ou use o Makefile:
    make docs-e2e
"""

import pytest
from pathlib import Path
from datetime import datetime
from playwright.async_api import Page
import asyncio
import os

from tests.e2e.utils import wait_for_react, wait_for_navigation_complete


# Pytest hook para adicionar opção --generate-docs
def pytest_addoption(parser):
    """Add custom pytest options"""
    parser.addoption(
        "--generate-docs",
        action="store_true",
        default=False,
        help="Generate visual documentation from tests"
    )


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


class DocumentationGenerator:
    """Helper class to generate documentation from tests"""
    
    def __init__(self, page: Page, output_dir: Path):
        self.page = page
        self.output_dir = output_dir
        self.screenshots = []
        self.steps = []
    
    def take_screenshot(self, name: str, description: str = ""):
        """Take a screenshot and save metadata"""
        screenshot_path = self.output_dir / f"{name}.png"
        self.page.screenshot(path=str(screenshot_path), full_page=True)
        
        self.screenshots.append({
            "name": name,
            "path": f"operacional/screenshots/{name}.png",
            "description": description,
            "timestamp": datetime.now().isoformat()
        })
        
        return screenshot_path
    
    def add_step(self, step_number: int, title: str, instructions: list, screenshot_name: str):
        """Add a documentation step"""
        screenshot_path = self.output_dir / f"{screenshot_name}.png"
        self.page.screenshot(path=str(screenshot_path), full_page=True)
        
        step = {
            "step": step_number,
            "title": title,
            "instructions": instructions,
            "screenshot": f"operacional/screenshots/{screenshot_name}.png",
            "screenshot_name": screenshot_name
        }
        
        self.steps.append(step)
        return step
    
    def generate_markdown(self, filename: str = "GUIA_VISUAL.md"):
        """Generate markdown documentation from screenshots"""
        md_path = self.output_dir.parent / filename
        md_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# 📖 Guia Visual - ForgeERP\n\n")
            f.write(f"Este guia foi gerado automaticamente pelos testes E2E.\n\n")
            f.write(f"**Gerado em:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            for i, screenshot in enumerate(self.screenshots, 1):
                f.write(f"## {i}. {screenshot['description']}\n\n")
                f.write(f"![{screenshot['name']}]({screenshot['path']})\n\n")
                f.write(f"**Descrição:** {screenshot['description']}\n\n")
                f.write("---\n\n")
        
        print(f"✅ Documentação gerada em: {md_path}")
    
    def generate_step_by_step_markdown(self, filename: str = "GUIA_PASSO_A_PASSO.md"):
        """Generate step-by-step markdown documentation"""
        md_path = self.output_dir.parent / filename
        md_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# 📖 Guia Passo a Passo - ForgeERP\n\n")
            f.write(f"Este guia foi gerado automaticamente pelos testes E2E.\n\n")
            f.write(f"**Gerado em:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            for step in self.steps:
                f.write(f"## Passo {step['step']}: {step['title']}\n\n")
                f.write(f"![{step['screenshot_name']}]({step['screenshot']})\n\n")
                
                f.write("### O que fazer:\n\n")
                for i, instruction in enumerate(step['instructions'], 1):
                    f.write(f"{i}. {instruction}\n")
                
                f.write("\n---\n\n")
        
        print(f"✅ Guia gerado em: {md_path}")


def test_login_documentation(page: Page, docs_output_dir: Path, should_generate_docs: bool, frontend_url: str):
    """Teste de login que gera documentação visual"""
    if not should_generate_docs:
        pytest.skip("Execute com --generate-docs para gerar documentação")
    
    generator = DocumentationGenerator(page, docs_output_dir)
    
    # Step 1: Access login page
    page.goto(frontend_url, wait_until="networkidle", timeout=30000)
    wait_for_react(page)
    generator.add_step(
        1,
        "Acessar a aplicação",
        [
            f"Abra o navegador e acesse: {frontend_url}",
            "A página de login será exibida automaticamente",
            "Você verá o formulário de login com campos para usuário e senha"
        ],
        "login_01_initial_page"
    )
    
    # Step 2: Fill username
    username_selectors = [
        'input[id="username"]',
        'input[type="text"]',
        'input[placeholder*="admin"]',
    ]
    username_filled = False
    for selector in username_selectors:
        try:
            input_field = page.locator(selector).first
            if input_field.count() > 0:
                input_field.fill("admin")
                username_filled = True
                break
        except:
            continue
    
    if username_filled:
        generator.add_step(
            2,
            "Preencher campo de usuário",
            [
                "No campo 'Usuário', digite: **admin**",
                "Este é o usuário padrão do sistema",
                "O campo aceita apenas texto"
            ],
            "login_02_username"
        )
    
    # Step 3: Fill password
    try:
        password_input = page.locator('input[type="password"]').first
        if password_input.count() > 0:
            password_input.fill("admin")
            generator.add_step(
                3,
                "Preencher campo de senha",
                [
                    "No campo 'Senha', digite: **admin**",
                    "Esta é a senha padrão do sistema",
                    "A senha é ocultada por segurança (aparece como ••••••••)"
                ],
                "login_03_password"
            )
    except Exception as e:
        print(f"⚠️  Não foi possível preencher senha: {e}")
    
    # Step 4: Submit
    submit_selectors = [
        'button[type="submit"]',
        'button:has-text("Entrar")',
        'button:has-text("Login")',
    ]
    submitted = False
    for selector in submit_selectors:
        try:
            button = page.locator(selector).first
            if button.count() > 0:
                button.click()
                time.sleep(3)
                wait_for_react(page)
                submitted = True
                generator.add_step(
                    4,
                    "Clicar em 'Entrar'",
                    [
                        "Clique no botão **'Entrar'**",
                        "O sistema irá validar suas credenciais",
                        "Se corretas, você será redirecionado para o dashboard"
                    ],
                    "login_04_success"
                )
                break
        except:
            continue
    
    # Generate documentation
    generator.generate_step_by_step_markdown()


def test_configuration_documentation(page: Page, docs_output_dir: Path, should_generate_docs: bool, frontend_url: str, api_url: str):
    """Teste de configurações que gera documentação visual"""
    if not should_generate_docs:
        pytest.skip("Execute com --generate-docs para gerar documentação")
    
    # Login first via API
    import requests
    response = requests.post(
        f"{api_url}/api/v1/auth/login",
        json={"username": "admin", "password": "admin"}
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        page.goto(frontend_url)
        page.evaluate(f"localStorage.setItem('token', '{token}')")
        page.reload()
        wait_for_react(page)
    
    generator = DocumentationGenerator(page, docs_output_dir)
    
    # Navigate to configurations
    try:
        config_selectors = [
            "text=Configurações",
            'button:has-text("Configurações")',
        ]
        for selector in config_selectors:
            try:
                element = page.locator(selector).first
                if element.count() > 0:
                    element.click()
                    wait_for_navigation_complete(page)
                    break
            except:
                continue
        
        generator.add_step(
            5,
            "Acessar página de configurações",
            [
                "Após fazer login, clique na aba **'Configurações'** no topo da página",
                "A página de configurações será exibida",
                "Você verá a lista de configurações existentes (se houver)"
            ],
            "config_01_page"
        )
    except Exception as e:
        print(f"⚠️  Não foi possível navegar para Configurações: {e}")
        return
    
    # Generate documentation
    generator.generate_step_by_step_markdown("GUIA_PASSO_A_PASSO.md")

