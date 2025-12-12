"""
Módulo para seleção interativa de linguagem no terminal.
"""
from typing import List, Optional


class LanguageSelector:
    """Classe para exibir e selecionar linguagem de destino no terminal."""
    
    # Linguagens disponíveis
    AVAILABLE_LANGUAGES = {
        '1': {'code': 'php', 'name': 'PHP', 'description': 'PHP 8.0+'},
        '2': {'code': 'python', 'name': 'Python', 'description': 'Python 3.8+'},
        '3': {'code': 'javascript', 'name': 'JavaScript', 'description': 'Node.js 14+'}
    }
    
    @staticmethod
    def display_languages() -> None:
        """
        Exibe a lista de linguagens disponíveis numerada no terminal.
        """
        print("\n" + "=" * 60)
        print("Escolha as linguagens de destino:")
        print("=" * 60)
        
        for key, lang_info in LanguageSelector.AVAILABLE_LANGUAGES.items():
            print(f"[{key}] {lang_info['name']} - {lang_info['description']}")
        
        print("=" * 60)
    
    @staticmethod
    def select_languages(default: Optional[str] = None) -> List[str]:
        """
        Permite que o usuário selecione múltiplas linguagens por índice.
        
        Args:
            default: Linguagem padrão (se None, pede seleção)
            
        Returns:
            Lista com códigos das linguagens selecionadas (ex: ['php', 'javascript'])
        """
        LanguageSelector.display_languages()
        
        # Se há uma linguagem padrão válida, mostra como opção
        default_option = None
        if default and default in [lang['code'] for lang in LanguageSelector.AVAILABLE_LANGUAGES.values()]:
            for key, lang_info in LanguageSelector.AVAILABLE_LANGUAGES.items():
                if lang_info['code'] == default:
                    default_option = key
                    break
        
        if default_option:
            print(f"\nLinguagem padrão configurada: {LanguageSelector.AVAILABLE_LANGUAGES[default_option]['name']}")
            print("Pressione Enter para usar apenas a padrão ou escolha múltiplas opções.")
        
        while True:
            try:
                selection = input("\nDigite os números separados por vírgula (Ex: 1,3) ou Enter para padrão: ").strip()
                
                # Se vazio e há padrão, usa apenas o padrão
                if not selection and default_option:
                    selected_code = LanguageSelector.AVAILABLE_LANGUAGES[default_option]['code']
                    selected_name = LanguageSelector.AVAILABLE_LANGUAGES[default_option]['name']
                    print(f"\n✓ Usando linguagem padrão: {selected_name}")
                    return [selected_code]
                
                # Se vazio e não há padrão, pede novamente
                if not selection:
                    print("Por favor, escolha pelo menos uma linguagem.")
                    continue
                
                # Processa a entrada (múltiplas seleções)
                indices = [x.strip() for x in selection.split(',')]
                
                # Valida os índices
                selected_languages = []
                invalid_indices = []
                
                for idx in indices:
                    if idx in LanguageSelector.AVAILABLE_LANGUAGES:
                        lang_code = LanguageSelector.AVAILABLE_LANGUAGES[idx]['code']
                        if lang_code not in selected_languages:  # Evita duplicatas
                            selected_languages.append(lang_code)
                    else:
                        invalid_indices.append(idx)
                
                if invalid_indices:
                    valid_options = ', '.join(LanguageSelector.AVAILABLE_LANGUAGES.keys())
                    print(f"Opções inválidas: {', '.join(invalid_indices)}")
                    print(f"Por favor, escolha números entre: {valid_options}")
                    continue
                
                if not selected_languages:
                    print("Nenhuma linguagem válida selecionada. Tente novamente.")
                    continue
                
                # Mostra linguagens selecionadas
                selected_names = [LanguageSelector.AVAILABLE_LANGUAGES[k]['name'] 
                                 for k, v in LanguageSelector.AVAILABLE_LANGUAGES.items() 
                                 if v['code'] in selected_languages]
                print(f"\n✓ {len(selected_languages)} linguagem(s) selecionada(s): {', '.join(selected_names)}")
                return selected_languages
                
            except KeyboardInterrupt:
                print("\n\nOperação cancelada pelo usuário.")
                # Retorna padrão se disponível, senão PHP
                if default and default in [lang['code'] for lang in LanguageSelector.AVAILABLE_LANGUAGES.values()]:
                    return [default]
                return ['php']
            except Exception as e:
                print(f"Erro ao processar seleção: {e}")
                continue
    
    @staticmethod
    def select_language(default: Optional[str] = None) -> str:
        """
        Método de compatibilidade: permite selecionar uma única linguagem.
        
        Args:
            default: Linguagem padrão (se None, pede seleção)
            
        Returns:
            Código da linguagem selecionada (ex: 'php', 'python', 'javascript')
        """
        languages = LanguageSelector.select_languages(default)
        return languages[0] if languages else (default or 'php')

