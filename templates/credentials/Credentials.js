/**
 * Classes de credenciais para APIs de IA
 * 
 * Este módulo fornece classes para gerenciar credenciais de diferentes
 * provedores de IA (OpenAI, Anthropic, OpenRouter, etc.)
 */

/**
 * Classe base abstrata para credenciais de API
 */
class Credentials {
    /**
     * Obtém a chave da API
     * 
     * @returns {string} Chave da API ou string vazia se não configurada
     */
    getApiKey() {
        throw new Error('Método getApiKey() deve ser implementado');
    }
}

/**
 * Credenciais para OpenAI
 */
class OpenAICredentials extends Credentials {
    /**
     * Construtor
     * 
     * @param {string|null} apiKey - Chave da API (opcional, usa variável de ambiente se não fornecida)
     */
    constructor(apiKey = null) {
        super();
        this._apiKey = apiKey;
    }
    
    /**
     * Obtém a chave da API OpenAI
     * 
     * @returns {string} Chave da API ou string vazia se não configurada
     */
    getApiKey() {
        if (this._apiKey) {
            return this._apiKey;
        }
        return process.env.OPENAI_API_KEY || '';
    }
}

/**
 * Credenciais para Anthropic (Claude)
 */
class AnthropicCredentials extends Credentials {
    /**
     * Construtor
     * 
     * @param {string|null} apiKey - Chave da API (opcional, usa variável de ambiente se não fornecida)
     */
    constructor(apiKey = null) {
        super();
        this._apiKey = apiKey;
    }
    
    /**
     * Obtém a chave da API Anthropic
     * 
     * @returns {string} Chave da API ou string vazia se não configurada
     */
    getApiKey() {
        if (this._apiKey) {
            return this._apiKey;
        }
        return process.env.ANTHROPIC_API_KEY || '';
    }
}

/**
 * Credenciais para OpenRouter
 */
class OpenRouterCredentials extends Credentials {
    /**
     * Construtor
     * 
     * @param {string|null} apiKey - Chave da API (opcional, usa variável de ambiente se não fornecida)
     */
    constructor(apiKey = null) {
        super();
        this._apiKey = apiKey;
    }
    
    /**
     * Obtém a chave da API OpenRouter
     * 
     * @returns {string} Chave da API ou string vazia se não configurada
     */
    getApiKey() {
        if (this._apiKey) {
            return this._apiKey;
        }
        return process.env.OPENROUTER_API_KEY || '';
    }
}

module.exports = {
    Credentials,
    OpenAICredentials,
    AnthropicCredentials,
    OpenRouterCredentials
};

