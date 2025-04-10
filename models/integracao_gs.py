import gspread
import pandas as pd
from utils.utils import texto_no_console

class IntegracaoGS:
    def __init__(self, conta_de_servico_json, nome_planilha, nome_aba):
        self.conta_de_servico_json=conta_de_servico_json
        self.nome_planilha=nome_planilha
        self.nome_aba=nome_aba
        pass

    def conectar(self):
        try:
            gc = gspread.service_account(filename=self.conta_de_servico_json)
            planilha_geral = gc.open(title=self.nome_planilha)
            texto_no_console('A conexão com o Google Sheets foi estabelecida com sucesso.')

            aba_conectada = planilha_geral.worksheet(self.nome_aba)
            return aba_conectada
        
        except gspread.exceptions.SpreadsheetNotFound:
            texto_no_console(f'Erro: Planilha com o nome "{self.nome_planilha}" não foi encontrada! Verifique o parâmetro x no arquivo de configuração.')
        except gspread.WorksheetNotFound:
            texto_no_console(f'Erro: A conecção com a planilha foi feita com sucesso, no entando não encontramos a aba selecionada na configuração. Aba informada: {self.nome_aba}.')
        except Exception as e:
            texto_no_console([f'Erro não tipificado: "{e}"', 'Verificar com o desenvolvedor.'])

    def retorno_google_planilhas_pandas(self, planilha_google, dados_necessarios=[]):
        try:
            planilha = planilha_google.get_all_records()
            planilha_pandas = pd.DataFrame(planilha)
            planilha_com_dados_necessarios = planilha_pandas[dados_necessarios]
            lista_de_lista = planilha_com_dados_necessarios.values.tolist()
            return lista_de_lista
        except AttributeError as e:
            texto_no_console(f'Erro: {e}')
        except KeyError as e:
            texto_no_console(f'Erro: {e}')
            return None
    

if __name__ == "__main__":
    conta = r'configs/conta_servico.json'
    app = IntegracaoGS(conta_de_servico_json=conta, nome_planilha='auto_experts', nome_aba='pag1')
    plan = app.conectar()
    print(plan.get_all_values())
