"""Main CLI application"""

import typer
import subprocess
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import Optional, List

app = typer.Typer(name="forge", help="ForgeERP CLI - Ferramenta de gerenciamento diário")
console = Console()


def _run_docker_compose(cmd: List[str], check: bool = True) -> tuple[int, str, str]:
    """Executa comando docker compose"""
    try:
        result = subprocess.run(
            ["docker", "compose"] + cmd,
            capture_output=True,
            text=True,
            check=check
        )
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError:
        console.print("[red]Erro: docker compose não encontrado. Instale o Docker primeiro.[/red]")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stdout, e.stderr


@app.command()
def up(
    build: bool = typer.Option(False, "--build", "-b", help="Construir imagens antes de subir"),
    detach: bool = typer.Option(True, "--detach", "-d", help="Executar em background")
):
    """Subir a aplicação"""
    console.print("[green]🚀 Subindo aplicação...[/green]")
    # Baixa imagem pré-compilada, se disponível
    console.print("[blue]📥 Verificando imagem no registro (GHCR)...[/blue]")
    _run_docker_compose(["--profile", "prod", "pull"], check=False)
    
    # Usa profile dev para build local, prod para imagem pré-compilada
    profile = "dev" if build else "prod"
    cmd = ["--profile", profile, "up"]
    if detach:
        cmd.append("-d")
    if build:
        cmd.append("--build")
    
    returncode, stdout, stderr = _run_docker_compose(cmd)
    if returncode == 0:
        console.print("[green]✅ Aplicação subida com sucesso![/green]")
        console.print(f"[dim]{stdout}[/dim]")
    else:
        console.print(f"[red]❌ Erro ao subir aplicação:[/red]\n{stderr}")
        sys.exit(returncode)


@app.command()
def down():
    """Parar a aplicação"""
    console.print("[yellow]🛑 Parando aplicação...[/yellow]")
    returncode, stdout, stderr = _run_docker_compose(["down"])
    if returncode == 0:
        console.print("[green]✅ Aplicação parada![/green]")
    else:
        console.print(f"[red]❌ Erro ao parar aplicação:[/red]\n{stderr}")
        sys.exit(returncode)


@app.command()
def restart(
    service: Optional[str] = typer.Argument(None, help="Serviço específico (backend, frontend)")
):
    """Reiniciar serviços"""
    if service:
        console.print(f"[yellow]🔄 Reiniciando {service}...[/yellow]")
        returncode, stdout, stderr = _run_docker_compose(["restart", service])
    else:
        console.print("[yellow]🔄 Reiniciando todos os serviços...[/yellow]")
        returncode, stdout, stderr = _run_docker_compose(["restart"])
    
    if returncode == 0:
        console.print("[green]✅ Serviços reiniciados![/green]")
    else:
        console.print(f"[red]❌ Erro ao reiniciar:[/red]\n{stderr}")
        sys.exit(returncode)


@app.command()
def logs(
    service: Optional[str] = typer.Argument(None, help="Serviço específico (backend, frontend)"),
    follow: bool = typer.Option(False, "--follow", "-f", help="Seguir logs"),
    tail: int = typer.Option(100, "--tail", "-n", help="Número de linhas")
):
    """Ver logs dos serviços"""
    cmd = ["logs", "--tail", str(tail)]
    if follow:
        cmd.append("-f")
    if service:
        cmd.append(service)
    
    returncode, stdout, stderr = _run_docker_compose(cmd, check=False)
    if stdout:
        console.print(stdout)
    if stderr:
        console.print(f"[dim]{stderr}[/dim]")


@app.command()
def status():
    """Status dos serviços"""
    console.print("[green]📊 Verificando status...[/green]\n")
    
    # Status dos containers
    returncode, stdout, stderr = _run_docker_compose(["ps"], check=False)
    if returncode == 0:
        console.print(Panel(stdout, title="[bold]Status dos Containers[/bold]", border_style="green"))
    
    # Health check da API
    try:
        import httpx
        response = httpx.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            console.print("[green]✅ API: Online[/green]")
        else:
            console.print(f"[yellow]⚠️  API: Status {response.status_code}[/yellow]")
    except Exception:
        console.print("[red]❌ API: Offline[/red]")


@app.command()
def user(
    username: str = typer.Option("admin", "--username", "-u", help="Nome de usuário"),
    password: str = typer.Option("admin", "--password", "-p", help="Senha"),
    email: str = typer.Option("admin@forgeerp.ai", "--email", "-e", help="Email"),
    create: bool = typer.Option(True, "--create", help="Criar usuário"),
):
    """Criar usuário admin"""
    if create:
        console.print(f"[green]👤 Criando usuário {username}...[/green]")
        cmd = [
            "exec", "-T", "backend",
            "python", "scripts/create_admin_user.py",
            "--username", username,
            "--password", password,
            "--email", email
        ]
        returncode, stdout, stderr = _run_docker_compose(cmd, check=False)
        if returncode == 0:
            console.print(f"[green]✅ Usuário {username} criado com sucesso![/green]")
            if stdout:
                console.print(f"[dim]{stdout}[/dim]")
        else:
            console.print(f"[red]❌ Erro ao criar usuário:[/red]\n{stderr}")
            sys.exit(returncode)


@app.command()
def test(
    unit: bool = typer.Option(False, "--unit", "-u", help="Testes unitários"),
    integration: bool = typer.Option(False, "--integration", "-i", help="Testes de integração"),
    e2e: bool = typer.Option(False, "--e2e", "-e", help="Testes E2E"),
    coverage: bool = typer.Option(False, "--coverage", "-c", help="Com cobertura"),
    all: bool = typer.Option(False, "--all", "-a", help="Todos os testes"),
):
    """Executar testes"""
    console.print("[green]🧪 Executando testes...[/green]")
    
    cmd = ["exec", "-T", "backend"]
    
    if all:
        cmd.extend(["make", "test"])
    elif unit:
        cmd.extend(["make", "test-unit"])
    elif integration:
        cmd.extend(["make", "test-integration"])
    elif e2e:
        cmd.extend(["make", "test-e2e"])
    elif coverage:
        cmd.extend(["make", "test-coverage"])
    else:
        cmd.extend(["make", "test"])
    
    returncode, stdout, stderr = _run_docker_compose(cmd, check=False)
    if stdout:
        console.print(stdout)
    if stderr:
        console.print(f"[dim]{stderr}[/dim]")
    
    if returncode != 0:
        sys.exit(returncode)


@app.command()
def update():
    """Atualizar aplicação"""
    console.print("[yellow]🔄 Atualizando aplicação...[/yellow]")
    
    # Pull do código
    console.print("[dim]📥 Baixando atualizações...[/dim]")
    try:
        subprocess.run(["git", "pull", "origin", "main"], check=True)
    except subprocess.CalledProcessError:
        console.print("[yellow]⚠️  Erro ao fazer git pull. Continue manualmente.[/yellow]")
    
    # Rebuild e restart
    console.print("[dim]🔨 Reconstruindo imagens...[/dim]")
    returncode, stdout, stderr = _run_docker_compose(["down"])
    
    returncode, stdout, stderr = _run_docker_compose(["up", "-d", "--build"])
    if returncode == 0:
        console.print("[green]✅ Aplicação atualizada com sucesso![/green]")
    else:
        console.print(f"[red]❌ Erro ao atualizar:[/red]\n{stderr}")
        sys.exit(returncode)


@app.command()
def clean():
    """Limpar cache e containers parados"""
    console.print("[yellow]🧹 Limpando...[/yellow]")
    
    # Parar e remover containers
    _run_docker_compose(["down"], check=False)
    
    # Limpar sistema Docker
    try:
        subprocess.run(["docker", "system", "prune", "-f"], check=False)
        console.print("[green]✅ Limpeza concluída![/green]")
    except Exception as e:
        console.print(f"[yellow]⚠️  Erro na limpeza: {e}[/yellow]")


@app.command()
def reset():
    """Resetar banco de dados (⚠️  CUIDADO: apaga todos os dados)"""
    confirm = typer.confirm("⚠️  Tem certeza? Isso irá apagar todos os dados!")
    if not confirm:
        console.print("[yellow]Operação cancelada.[/yellow]")
        return
    
    console.print("[yellow]🔄 Resetando banco de dados...[/yellow]")
    
    # Parar serviços
    _run_docker_compose(["down"], check=False)
    
    # Remover banco
    db_path = Path("data/forgeerp.db")
    if db_path.exists():
        db_path.unlink()
        console.print("[green]✅ Banco de dados removido![/green]")
    
    # Subir novamente
    returncode, stdout, stderr = _run_docker_compose(["up", "-d"])
    if returncode == 0:
        console.print("[green]✅ Aplicação reiniciada![/green]")
        console.print("[yellow]💡 Execute 'forge user' para criar um novo usuário admin.[/yellow]")
    else:
        console.print(f"[red]❌ Erro ao reiniciar:[/red]\n{stderr}")
        sys.exit(returncode)


@app.command()
def init():
    """Inicializar novo fork do ForgeERP"""
    console.print("[green]🚀 Inicializando ForgeERP...[/green]")
    console.print("[yellow]Funcionalidade em desenvolvimento[/yellow]")


@app.command()
def setup():
    """Onboarding interativo"""
    console.print("[green]⚙️  Iniciando onboarding...[/green]")
    console.print("[yellow]Funcionalidade em desenvolvimento[/yellow]")


if __name__ == "__main__":
    app()
