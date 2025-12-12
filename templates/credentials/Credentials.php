<?php

/**
 * Classe base para credenciais de APIs
 * 
 * Esta classe fornece acesso centralizado às credenciais de APIs,
 * carregando-as de variáveis de ambiente ou permitindo injeção direta.
 * 
 * @package Generated\Credentials
 */
abstract class Credentials {
    
    /**
     * Obtém uma credencial de variável de ambiente
     * 
     * @param string $key Nome da variável de ambiente
     * @param string $default Valor padrão se não encontrado
     * @return string Valor da credencial
     */
    protected static function getEnv(string $key, string $default = ''): string
    {
        $value = getenv($key);
        return $value !== false ? $value : $default;
    }
    
    /**
     * Valida se uma credencial está configurada
     * 
     * @param string $value Valor da credencial
     * @param string $name Nome da credencial (para mensagem de erro)
     * @throws \RuntimeException Se a credencial não estiver configurada
     */
    protected static function validate(string $value, string $name): void
    {
        if (empty($value)) {
            throw new \RuntimeException(
                "Credencial '{$name}' não configurada. " .
                "Configure a variável de ambiente ou passe via construtor."
            );
        }
    }
}

/**
 * Credenciais para OpenAI
 * 
 * @package Generated\Credentials
 */
class OpenAICredentials extends Credentials {
    
    private string $apiKey;
    
    /**
     * @param string|null $apiKey Chave da API (opcional, usa OPENAI_API_KEY se não fornecido)
     */
    public function __construct(?string $apiKey = null)
    {
        $this->apiKey = $apiKey ?? self::getEnv('OPENAI_API_KEY', '');
        self::validate($this->apiKey, 'OPENAI_API_KEY');
    }
    
    public function getApiKey(): string
    {
        return $this->apiKey;
    }
}

/**
 * Credenciais para Anthropic (Claude)
 * 
 * @package Generated\Credentials
 */
class AnthropicCredentials extends Credentials {
    
    private string $apiKey;
    
    /**
     * @param string|null $apiKey Chave da API (opcional, usa ANTHROPIC_API_KEY se não fornecido)
     */
    public function __construct(?string $apiKey = null)
    {
        $this->apiKey = $apiKey ?? self::getEnv('ANTHROPIC_API_KEY', '');
        self::validate($this->apiKey, 'ANTHROPIC_API_KEY');
    }
    
    public function getApiKey(): string
    {
        return $this->apiKey;
    }
}

/**
 * Credenciais para OpenRouter
 * 
 * @package Generated\Credentials
 */
class OpenRouterCredentials extends Credentials {
    
    private string $apiKey;
    
    /**
     * @param string|null $apiKey Chave da API (opcional, usa OPENROUTER_API_KEY se não fornecido)
     */
    public function __construct(?string $apiKey = null)
    {
        $this->apiKey = $apiKey ?? self::getEnv('OPENROUTER_API_KEY', '');
        self::validate($this->apiKey, 'OPENROUTER_API_KEY');
    }
    
    public function getApiKey(): string
    {
        return $this->apiKey;
    }
}

