<!-- # Laravel AI SDK -->
# Laravel AI SDK

- [Introduction](#introduction)
- [Installation](#installation)
    - [Configuration](#configuration)
    - [Custom Base URLs](#custom-base-urls)
    - [OpenAI-Compatible Providers](#openai-compatible-providers)
    - [Provider Support](#provider-support)
- [Agents](#agents)
    - [Prompting](#prompting)
    - [Conversation Context](#conversation-context)
    - [Structured Output](#structured-output)
    - [Attachments](#attachments)
    - [Streaming](#streaming)
    - [Broadcasting](#broadcasting)
    - [Queueing](#queueing)
    - [Tools](#tools)
    - [Deferred Tool Loading](#deferred-tool-loading)
    - [File Storage Tools](#file-storage-tools)
    - [MCP Tools](#mcp-tools)
    - [Provider Tools](#provider-tools)
    - [Sub-Agents](#sub-agents)
    - [Middleware](#middleware)
    - [Anonymous Agents](#anonymous-agents)
    - [Agent Configuration](#agent-configuration)
    - [Provider Options](#provider-options)
    - [Prompt Caching](#prompt-caching)
- [Human Tool Approval](#human-tool-approval)
    - [Complete Approval Flow](#complete-approval-flow)
- [Images](#images)
- [Audio (TTS)](#audio)
- [Transcription (STT)](#transcription)
- [Text Summarization](#text-summarization)
- [Embeddings](#embeddings)
    - [Multimodal Embeddings](#multimodal-embeddings)
    - [Querying Embeddings](#querying-embeddings)
    - [Caching Embeddings](#caching-embeddings)
- [Reranking](#reranking)
- [Classification](#classification)
- [Files](#files)
- [Vector Stores](#vector-stores)
    - [Adding Files to Stores](#adding-files-to-stores)
- [Usage](#usage)
- [Failover](#failover)
- [Testing](#testing)
    - [Agents](#testing-agents)
    - [Images](#testing-images)
    - [Audio](#testing-audio)
    - [Transcriptions](#testing-transcriptions)
    - [Embeddings](#testing-embeddings)
    - [Reranking](#testing-reranking)
    - [Classification](#testing-classification)
    - [Files](#testing-files)
    - [Vector Stores](#testing-vector-stores)
- [Events](#events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- The [Laravel AI SDK](https://github.com/laravel/ai) provides a unified, expressive API for interacting with AI providers such as OpenAI, Anthropic, Gemini, and more. With the AI SDK, you can build intelligent agents with tools and structured output, generate images, synthesize and transcribe audio, create vector embeddings, and much more — all using a consistent, Laravel-friendly interface. -->
[Laravel AI SDK](https://github.com/laravel/ai)는 OpenAI, Anthropic, Gemini 등 다양한 AI 프로바이더와 상호작용할 수 있는 통합되고 표현력 있는 API를 제공합니다. AI SDK를 사용하면 일관된 Laravel 친화적 인터페이스만으로 도구와 구조화된 출력을 갖춘 지능형 에이전트를 만들고, 이미지를 생성하며, 오디오를 합성하고 전사하고, 벡터 임베딩을 생성하는 등 다양한 작업을 수행할 수 있습니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- You can install the Laravel AI SDK via Composer: -->
Composer를 통해 Laravel AI SDK를 설치할 수 있습니다.

```shell
composer require laravel/ai
```

<!-- Next, you should publish the AI SDK configuration and migration files using the `vendor:publish` Artisan command: -->
다음으로, `vendor:publish` Artisan 명령어를 사용하여 AI SDK 설정 파일과 마이그레이션 파일을 게시해야 합니다.

```shell
php artisan vendor:publish --provider="Laravel\Ai\AiServiceProvider"
```

<!-- Finally, you should run your application's database migrations. This will create a `agent_conversations` and `agent_conversation_messages` table that the AI SDK uses to power its conversation storage: -->
마지막으로 애플리케이션의 데이터베이스 마이그레이션을 실행해야 합니다. 이 작업은 AI SDK가 대화 저장 기능을 제공하는 데 사용하는 `agent_conversations` 및 `agent_conversation_messages` 테이블을 생성합니다.

```shell
php artisan migrate
```

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- You may define your AI provider credentials in your application's `config/ai.php` configuration file or as environment variables in your application's `.env` file: -->
AI 프로바이더 자격 증명은 애플리케이션의 `config/ai.php` 설정 파일 또는 애플리케이션의 `.env` 파일에 환경 변수로 정의할 수 있습니다.

```ini
ANTHROPIC_API_KEY=
AZURE_OPENAI_API_KEY=
COHERE_API_KEY=
DEEPSEEK_API_KEY=
ELEVENLABS_API_KEY=
GEMINI_API_KEY=
GROQ_API_KEY=
MISTRAL_API_KEY=
OLLAMA_API_KEY=
OPENAI_API_KEY=
OPENAI_COMPATIBLE_API_KEY=
OPENAI_COMPATIBLE_URL=
OPENROUTER_API_KEY=
JINA_API_KEY=
TYPESAFE_API_KEY=
VOYAGEAI_API_KEY=
XAI_API_KEY=
```

<!-- The default models used for text, images, audio, transcription, and embeddings may also be configured in your application's `config/ai.php` configuration file. -->
텍스트, 이미지, 오디오, 전사, 임베딩에 사용할 기본 모델도 애플리케이션의 `config/ai.php` 설정 파일에서 구성할 수 있습니다.

<a name="custom-base-urls"></a>
<!-- ### Custom Base URLs -->
### Custom Base URLs

<!-- By default, the Laravel AI SDK connects directly to each provider's public API endpoint. However, you may need to route requests through a different endpoint - for example, when using a proxy service to centralize API key management, implement rate limiting, or route traffic through a corporate gateway. -->
기본적으로 Laravel AI SDK는 각 프로바이더의 공개 API 엔드포인트에 직접 연결합니다. 하지만 다른 엔드포인트를 통해 요청을 라우팅해야 할 수도 있습니다. 예를 들어 API 키 관리를 중앙화하거나, 속도 제한을 구현하거나, 회사 게이트웨이를 통해 트래픽을 라우팅하기 위해 프록시 서비스를 사용할 때가 그렇습니다.

<!-- You may configure custom base URLs by adding a `url` parameter to your provider configuration: -->
프로바이더 설정에 `url` 매개변수를 추가하여 사용자 지정 Base URL을 구성할 수 있습니다.

```php
'providers' => [
    'openai' => [
        'driver' => 'openai',
        'key' => env('OPENAI_API_KEY'),
        'url' => env('OPENAI_URL'),
    ],

    'anthropic' => [
        'driver' => 'anthropic',
        'key' => env('ANTHROPIC_API_KEY'),
        'url' => env('ANTHROPIC_BASE_URL'),
    ],
],
```

<!-- This is useful when routing requests through a proxy service (such as LiteLLM or Azure OpenAI Gateway) or using alternative endpoints. -->
이는 LiteLLM 또는 Azure OpenAI Gateway와 같은 프록시 서비스를 통해 요청을 라우팅하거나 대체 엔드포인트를 사용할 때 유용합니다.

<!-- Custom base URLs are supported for the following providers: OpenAI, Anthropic, Gemini, Groq, Cohere, DeepSeek, xAI, and OpenRouter. -->
사용자 지정 Base URL은 다음 프로바이더에서 지원됩니다: OpenAI, Anthropic, Gemini, Groq, Cohere, DeepSeek, xAI, OpenRouter.

<a name="openai-compatible-providers"></a>
<!-- ### OpenAI-Compatible Providers -->
### OpenAI-Compatible Providers

<!-- If you are using an OpenAI-compatible API, such as LM Studio, vLLM, Together, Fireworks, or a local gateway, you may configure an `openai-compatible` provider. The `url` option is required, while the `key` option is optional and will be sent as a bearer token when present: -->
OpenAI 호환 API를 사용하고 있다면, LM Studio, vLLM, Together, Fireworks 또는 로컬 게이트웨이와 같은 API에 대해 `openai-compatible` 프로바이더를 구성할 수 있습니다. `url` 옵션은 필수이며, `key` 옵션은 선택 사항이고 값이 있으면 bearer token으로 전송됩니다:

```php
'providers' => [
    'local' => [
        'driver' => 'openai-compatible',
        'url' => env('LOCAL_AI_URL'),
        'key' => env('LOCAL_AI_API_KEY'),
    ],
],
```

<!-- Once configured, you may use the named provider like any other provider: -->
구성한 후에는 다른 프로바이더와 마찬가지로 이름이 지정된 프로바이더를 사용할 수 있습니다:

```php
agent()->prompt('What is Laravel?', provider: 'local', model: 'local-model');
```

<!-- You may also configure a default text model for the provider so that you do not need to pass a model explicitly: -->
프로바이더에 대한 기본 텍스트 모델도 구성할 수 있으므로, 모델을 명시적으로 전달할 필요가 없습니다:

```php
'local' => [
    'driver' => 'openai-compatible',
    'url' => env('LOCAL_AI_URL'),
    'key' => env('LOCAL_AI_API_KEY'),
    'models' => [
        'text' => [
            'default' => env('LOCAL_AI_MODEL'),
        ],
    ],
],
```

<!-- You may add custom HTTP headers to every outgoing request for the provider by defining a `headers` array in its configuration. This is useful when an endpoint requires an additional identifying or authentication header beyond the bearer token: -->
프로바이더의 모든 발신 요청에 사용자 지정 HTTP 헤더를 추가하려면 해당 설정에 `headers` 배열을 정의하면 됩니다. 엔드포인트에 bearer 토큰 외에 추가 식별 또는 인증 헤더가 필요한 경우 유용합니다.

```php
'local' => [
    'driver' => 'openai-compatible',
    'url' => env('LOCAL_AI_URL'),
    'key' => env('LOCAL_AI_API_KEY'),
    'headers' => [
        'X-Tenant-Id' => env('LOCAL_AI_TENANT_ID'),
    ],
],
```

<!-- OpenAI-compatible providers support text generation, streaming, tools, structured output, image attachments, embeddings, and transcription. If your endpoint requires additional request body fields, provide them using [provider options](#provider-options). -->
OpenAI 호환 프로바이더는 텍스트 생성, 스트리밍, 툴, 구조화 출력, 이미지 첨부 파일, 임베딩, 전사를 지원합니다. 엔드포인트에 추가 요청 본문 필드가 필요하다면 [provider options](#provider-options)를 사용해 지정할 수 있습니다.

<a name="openai-compatible-embeddings"></a>
<!-- #### OpenAI-Compatible Embeddings -->
#### OpenAI-Compatible Embeddings

<!-- Since arbitrary endpoints have no known models, you must configure a default embeddings model to use `embeddings()` with an OpenAI-compatible provider. You may also configure a fixed dimensions value; if omitted, the request is sent without a `dimensions` parameter and the model's native dimensions are used. -->
임의의 엔드포인트에는 알려진 모델이 없으므로, OpenAI 호환 프로바이더에서 `embeddings()`를 사용하려면 기본 임베딩 모델을 설정해야 합니다. 고정된 차원 값도 설정할 수 있으며, 생략하면 `dimensions` 파라미터 없이 요청을 보내고 모델의 기본 차원을 사용합니다.

```php
'local' => [
    'driver' => 'openai-compatible',
    'url' => env('LOCAL_AI_URL'),
    'key' => env('LOCAL_AI_API_KEY'),
    'models' => [
        'embeddings' => [
            'default' => 'text-embedding-qwen3-embedding-0.6b',
            'dimensions' => 1024, // optional
        ],
    ],
],
```

<a name="openai-compatible-transcriptions"></a>
<!-- #### OpenAI-Compatible Transcriptions -->
#### OpenAI-Compatible Transcriptions

<!-- Likewise, you must configure a default transcription model to use `Transcription` with an OpenAI-compatible provider. The audio will be uploaded to the endpoint's `/audio/transcriptions` route as a standard multipart request: -->
마찬가지로 OpenAI 호환 프로바이더와 함께 `Transcription`을 사용하도록 기본 전사 모델을 구성해야 합니다. 오디오는 표준 multipart 요청으로 엔드포인트의 `/audio/transcriptions` 라우트에 업로드됩니다:

```php
'local' => [
    'driver' => 'openai-compatible',
    'url' => env('LOCAL_AI_URL'),
    'key' => env('LOCAL_AI_API_KEY'),
    'models' => [
        'transcription' => [
            'default' => 'whisper-1',
        ],
    ],
],
```

> [!NOTE]
> OpenAI-compatible 및 Groq 프로바이더는 화자 분리를 지원하지 않습니다. 이러한 프로바이더를 사용할 때 `diarize` 메서드를 호출하면 예외가 발생합니다.

<a name="provider-support"></a>
<!-- ### Provider Support -->
### Provider Support

<!-- The AI SDK supports a variety of providers across its features. The following table summarizes which providers are available for each feature: -->
AI SDK는 다양한 기능에서 여러 프로바이더를 지원합니다. 다음 표는 각 기능에서 사용할 수 있는 프로바이더를 요약한 것입니다.

<div class="overflow-auto">

<!-- | Feature | Providers | |---|---| | Text | OpenAI, OpenAI Compatible, Anthropic, Gemini, Azure, Bedrock, Groq, xAI, DeepSeek, Mistral, Ollama, OpenRouter | | Images | OpenAI, Gemini, xAI, Azure, Bedrock, OpenRouter | | TTS | OpenAI, ElevenLabs, Gemini, Mistral, OpenRouter | | STT | OpenAI, OpenAI Compatible, ElevenLabs, Groq, Mistral, Gemini, OpenRouter | | Embeddings | OpenAI, OpenAI Compatible, Gemini, Azure, Bedrock, Cohere, Mistral, Jina, VoyageAI, Ollama, OpenRouter | | Reranking | Cohere, Jina, VoyageAI, Bedrock, OpenRouter | | Classification | TypeSafe, OpenRouter | | Files | OpenAI, Anthropic, Gemini, Azure, OpenRouter | -->
| 기능 | 프로바이더 |
|---|---|
| 텍스트 | OpenAI, OpenAI Compatible, Anthropic, Gemini, Azure, Bedrock, Groq, xAI, DeepSeek, Mistral, Ollama, OpenRouter |
| 이미지 | OpenAI, Gemini, xAI, Azure, Bedrock, OpenRouter |
| TTS | OpenAI, ElevenLabs, Gemini, Mistral, OpenRouter |
| STT | OpenAI, OpenAI Compatible, ElevenLabs, Groq, Mistral, Gemini, OpenRouter |
| 임베딩 | OpenAI, OpenAI Compatible, Gemini, Azure, Bedrock, Cohere, Mistral, Jina, VoyageAI, Ollama, OpenRouter |
| 리랭킹 | Cohere, Jina, VoyageAI, Bedrock, OpenRouter |
| 분류 | TypeSafe, OpenRouter |
| 파일 | OpenAI, Anthropic, Gemini, Azure, OpenRouter |

</div>

<!-- The `Laravel\Ai\Enums\Lab` enum may be used to reference providers throughout your code instead of using plain strings: -->
코드 전체에서 일반 문자열 대신 `Laravel\Ai\Enums\Lab` enum을 사용하여 프로바이더를 참조할 수 있습니다.

```php
use Laravel\Ai\Enums\Lab;

Lab::Anthropic;
Lab::OpenAI;
Lab::OpenAiCompatible;
Lab::Gemini;
// ...
```

<a name="agents"></a>
<!-- ## Agents -->
## Agents

<!-- Agents are the fundamental building block for interacting with AI providers in the Laravel AI SDK. Each agent is a dedicated PHP class that encapsulates the instructions, conversation context, tools, and output schema needed to interact with a large language model. Think of an agent as a specialized assistant — a sales coach, a document analyzer, a support bot — that you configure once and prompt as needed throughout your application. -->
에이전트는 Laravel AI SDK에서 AI 프로바이더와 상호작용하기 위한 기본 구성 요소입니다. 각 에이전트는 대규모 언어 모델과 상호작용하는 데 필요한 지침, 대화 컨텍스트, 도구, 출력 스키마를 캡슐화하는 전용 PHP 클래스입니다. 에이전트를 영업 코치, 문서 분석기, 지원 봇처럼 애플리케이션 전반에서 한 번 구성해 두고 필요할 때 프롬프트할 수 있는 특화된 어시스턴트라고 생각하면 됩니다.

<!-- You can create an agent via the `make:agent` Artisan command: -->
`make:agent` Artisan 명령어를 통해 에이전트를 만들 수 있습니다.

```shell
php artisan make:agent SalesCoach

php artisan make:agent SalesCoach --structured
```

<!-- Within the generated agent class, you can define the system prompt / instructions, message context, available tools, and output schema (if applicable): -->
생성된 에이전트 클래스 안에서 시스템 프롬프트 / 지침, 메시지 컨텍스트, 사용 가능한 도구, 출력 스키마(해당하는 경우)를 정의할 수 있습니다.

```php
<?php

namespace App\Ai\Agents;

use App\Ai\Tools\RetrievePreviousTranscripts;
use App\Models\History;
use App\Models\User;
use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\Conversational;
use Laravel\Ai\Contracts\HasStructuredOutput;
use Laravel\Ai\Contracts\HasTools;
use Laravel\Ai\Messages\Message;
use Laravel\Ai\Promptable;
use Stringable;

class SalesCoach implements Agent, Conversational, HasTools, HasStructuredOutput
{
    use Promptable;

    public function __construct(public User $user) {}

    /**
     * Get the instructions that the agent should follow.
     */
    public function instructions(): Stringable|string
    {
        return 'You are a sales coach, analyzing transcripts and providing feedback and an overall sales strength score.';
    }

    /**
     * Get the list of messages comprising the conversation so far.
     */
    public function messages(): iterable
    {
        return History::where('user_id', $this->user->id)
            ->latest()
            ->limit(50)
            ->get()
            ->reverse()
            ->map(function ($message) {
                return new Message($message->role, $message->content);
            })->all();
    }

    /**
     * Get the tools available to the agent.
     *
     * @return Tool[]
     */
    public function tools(): iterable
    {
        return [
            new RetrievePreviousTranscripts,
        ];
    }

    /**
     * Get the agent's structured output schema definition.
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'feedback' => $schema->string()->required(),
            'score' => $schema->integer()->min(1)->max(10)->required(),
        ];
    }
}
```

<a name="prompting"></a>
<!-- ### Prompting -->
### Prompting

<!-- To prompt an agent, first create an instance using the `make` method or standard instantiation, then call `prompt`: -->
에이전트에 프롬프트하려면 먼저 `make` 메서드 또는 일반적인 인스턴스 생성 방식으로 인스턴스를 만든 다음 `prompt`를 호출합니다.

```php
$response = (new SalesCoach)
    ->prompt('Analyze this sales transcript...');

return (string) $response;
```

<!-- The `make` method resolves your agent from the container, allowing automatic dependency injection. You may also pass arguments to the agent's constructor: -->
`make` 메서드는 컨테이너에서 에이전트를 해석하므로 자동 의존성 주입을 사용할 수 있습니다. 에이전트 생성자에 인수를 전달할 수도 있습니다.

```php
$agent = SalesCoach::make(user: $user);
```

<!-- By passing additional arguments to the `prompt` method, you may override the default provider, model, or HTTP timeout when prompting: -->
`prompt` 메서드에 추가 인수를 전달하면 프롬프트할 때 기본 프로바이더, 모델 또는 HTTP 제한 시간을 재정의할 수 있습니다.

```php
$response = (new SalesCoach)->prompt(
    'Analyze this sales transcript...',
    provider: Lab::Anthropic,
    model: 'claude-sonnet-5',
    timeout: 120,
);
```

<a name="raw-http-responses"></a>
<!-- #### Raw HTTP Responses -->
#### Raw HTTP Responses

<!-- Every response returned from a text-generating agent exposes the raw HTTP response from the underlying provider API call via a `raw` property. This gives you access to provider-specific information that isn't part of the AI SDK's generic response - rate-limit headers, request IDs, or other exact payload fields: -->
텍스트를 생성하는 에이전트가 반환하는 모든 응답은 `raw` 프로퍼티를 통해 내부에서 호출한 프로바이더 API의 원시 HTTP 응답을 제공합니다. 이를 통해 AI SDK의 일반 응답에는 포함되지 않는 프로바이더별 정보, 즉 속도 제한 헤더, 요청 ID 또는 기타 정확한 페이로드 필드에 액세스할 수 있습니다:

```php
$response = (new SalesCoach)->prompt('Analyze this sales transcript...');

$response->raw; // Illuminate\Http\Client\Response|null

$response->raw->header('X-RateLimit-Remaining-Requests');
$response->raw->json('id');
```

<!-- In a tool-call loop, each step retains the raw response of its own request: -->
툴 호출 루프에서 각 단계는 자체 요청의 원시 응답을 유지합니다:

```php
foreach ($response->steps as $step) {
    $step->raw?->header('X-RateLimit-Remaining-Requests');
}
```

> [!NOTE]
> 응답을 스트리밍하거나, HTTP 클라이언트 대신 AWS SDK를 통해 API를 호출하는 Bedrock provider를 사용하거나, `withRawResponse`를 통해 명시적으로 제공하지 않은 가짜 응답에서는 `raw` 프로퍼티가 `null`입니다.

<a name="conversation-context"></a>
<!-- ### Conversation Context -->
### Conversation Context

<!-- If your agent implements the `Conversational` interface, you may use the `messages` method to return the previous conversation context, if applicable: -->
에이전트가 `Conversational` 인터페이스를 구현하는 경우, 해당된다면 `messages` 메서드를 사용하여 이전 대화 컨텍스트를 반환할 수 있습니다.

```php
/**
 * Get the list of messages comprising the conversation so far.
 */
public function messages(): iterable
{
    return $this->user->history()
        ->latest()
        ->limit(50)
        ->get()
        ->reverse()
        ->map(fn ($message) => new Message(
            $message->role, $message->content,
        ))->all();
}
```

<!-- If your agent does not implement the `Conversational` interface, you may use the `withMessages` method to provide the conversation history for a single run, such as a history posted by your application's frontend: -->
에이전트가 `Conversational` 인터페이스를 구현하지 않는다면, 애플리케이션의 프런트엔드에서 게시한 기록처럼 단일 실행에 사용할 대화 기록을 제공하기 위해 `withMessages` 메서드를 사용할 수 있습니다.

```php
use Laravel\Ai\Messages\Message;

$response = (new SalesCoach)
    ->withMessages([
        new Message('user', 'Analyze this sales transcript...'),
        new Message('assistant', 'The rep never asked for the close.'),
    ])
    ->prompt('What should they say next time?');
```

<!-- Agents that implement the `Conversational` interface load their own history, so combining the two approaches will throw a `LogicException`. -->
`Conversational` 인터페이스를 구현하는 에이전트는 자체 기록을 로드하므로 두 접근 방식을 결합하면 `LogicException`이 발생합니다.

<a name="remembering-conversations"></a>
<!-- #### Remembering Conversations -->
#### Remembering Conversations

> [!WARNING]
> `RemembersConversations` 트레이트를 사용하기 전에 `vendor:publish` Artisan 명령어를 사용해 AI SDK 마이그레이션을 게시하고 실행해야 합니다. 이 마이그레이션은 대화를 저장하는 데 필요한 데이터베이스 테이블을 생성합니다.

<!-- If you would like Laravel to automatically store and retrieve conversation history for your agent, you may use the `RemembersConversations` trait. This trait provides a simple way to persist conversation messages to the database without manually implementing the `Conversational` interface: -->
Laravel이 에이전트의 대화 기록을 자동으로 저장하고 가져오도록 하려면 `RemembersConversations` trait를 사용할 수 있습니다. 이 trait는 `Conversational` 인터페이스를 직접 구현하지 않아도 대화 메시지를 데이터베이스에 유지할 수 있는 간단한 방법을 제공합니다.

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Concerns\RemembersConversations;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\Conversational;
use Laravel\Ai\Promptable;

class SalesCoach implements Agent, Conversational
{
    use Promptable, RemembersConversations;

    /**
     * Get the instructions that the agent should follow.
     */
    public function instructions(): string
    {
        return 'You are a sales coach...';
    }
}
```

<!-- When using the `RemembersConversations` trait, do not manually define a `messages` method in your agent class. If a `messages` method is present, it will take precedence over the trait's implementation and conversation history will not be loaded from the database. -->
`RemembersConversations` trait를 사용할 때는 에이전트 클래스에 `messages` 메서드를 직접 정의하지 마십시오. `messages` 메서드가 존재하면 trait의 구현보다 우선하게 되어 대화 기록이 데이터베이스에서 로드되지 않습니다.

<!-- To start a new conversation for a user, call the `forUser` method before prompting: -->
사용자에 대해 새 대화를 시작하려면 프롬프트하기 전에 `forUser` 메서드를 호출합니다.

```php
$response = (new SalesCoach)->forUser($user)->prompt('Hello!');

$conversationId = $response->conversationId;
```

<!-- The conversation ID is returned on the response and can be stored for future reference. If you would like to retrieve all of a user's conversations using Eloquent, you may add the `HasConversations` trait to your user model: -->
대화 ID는 응답에서 반환되며 나중에 참조할 수 있도록 저장할 수 있습니다. Eloquent를 사용하여 사용자의 모든 대화를 조회하고 싶다면 사용자 모델에 `HasConversations` trait를 추가할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Laravel\Ai\Concerns\HasConversations;

class User extends Authenticatable
{
    use HasConversations;
}
```

<!-- Once the trait has been added to your model, you may retrieve and query the user's conversations via the `conversations` relationship: -->
모델에 trait를 추가한 후에는 `conversations` 연관관계를 통해 사용자의 대화를 조회하고 쿼리할 수 있습니다:

```php
$conversations = $user->conversations()
    ->latest('updated_at')
    ->paginate(20);
```

<!-- To continue an existing conversation, use the `continue` method: -->
기존 대화를 이어가려면 `continue` 메서드를 사용합니다.

```php
$response = (new SalesCoach)
    ->continue($conversationId, as: $user)
    ->prompt('Tell me more about that.');
```

<!-- The `continueOrStart` method may be used to continue the given conversation, or start a new conversation if the given ID is `null`: -->
`continueOrStart` 메서드를 사용하면 주어진 대화를 계속 진행하거나, 주어진 ID가 `null`인 경우 새 대화를 시작할 수 있습니다:

```php
$response = (new SalesCoach)
    ->continueOrStart($conversationId, as: $user)
    ->prompt('Hello!');
```

<!-- When using the `RemembersConversations` trait, previous messages are automatically loaded and included in the conversation context when prompting. New messages (both user and assistant) are automatically stored after each interaction. Each response also contains the IDs of the conversation and messages that were stored: -->
`RemembersConversations` 트레이트를 사용하면 프롬프트를 보낼 때 이전 메시지가 자동으로 로드되어 대화 컨텍스트에 포함됩니다. 새로운 메시지(사용자와 어시스턴트의 메시지 모두)는 각 상호작용 후 자동으로 저장됩니다. 각 응답에는 저장된 대화와 메시지의 ID도 포함됩니다.

```php
$response->conversationId;
$response->userMessageId;
$response->assistantMessageId;
```

<a name="conversation-participants"></a>
<!-- #### Conversation Participants -->
#### Conversation Participants

<!-- Although users are the most common conversation participants, conversations may belong to any Eloquent model. Use the `forParticipant` method to start a conversation for another type of model: -->
사용자가 가장 일반적인 대화 참여자이지만, 대화는 어떤 Eloquent 모델에든 속할 수 있습니다. 다른 유형의 모델에 대한 대화를 시작하려면 `forParticipant` 메서드를 사용합니다.

```php
$response = (new SalesCoach)
    ->forParticipant($team)
    ->prompt('Review our latest sales results.');
```

<!-- The participant's morph class and primary key are stored with the conversation. Therefore, models of different types that have the same primary key, such as `User` ID `1` and `Team` ID `1`, have separate conversation histories. The `forUser` method is an alias for `forParticipant`. -->
참여자의 morph 클래스와 기본 키는 대화에 저장됩니다. 따라서 `User` ID `1`과 `Team` ID `1`처럼 기본 키가 같더라도 서로 다른 타입의 모델은 별도의 대화 기록을 가집니다. `forUser` 메서드는 `forParticipant`의 별칭입니다.

<!-- You may continue the participant's most recent conversation with the agent using the `continueLastConversation` method. Conversations are scoped to the agent, so only conversations that the agent participated in will be continued: -->
`continueLastConversation` 메서드를 사용하면 참가자가 에이전트와 나눈 가장 최근 대화를 계속 이어갈 수 있습니다. 대화는 에이전트별로 구분되므로 해당 에이전트가 참여한 대화만 계속 이어갈 수 있습니다:

```php
$response = (new SalesCoach)
    ->continueLastConversation($team)
    ->prompt('Tell me more about that.');
```

<!-- When continuing a specific conversation, pass the participant to the `continue` method: -->
특정 대화를 계속하려면 participant를 `continue` 메서드에 전달합니다:

```php
$response = (new SalesCoach)
    ->continue($conversationId, as: $team)
    ->prompt('Tell me more about that.');
```

<!-- The `HasConversations` trait may be added to any Eloquent model that participates in conversations. The resulting `conversations` relationship is a polymorphic relationship scoped to that model's type and primary key. You may also access the participant that owns a conversation through its inverse relationship: -->
`HasConversations` 트레이트는 대화에 참여하는 모든 Eloquent 모델에 추가할 수 있습니다. 이렇게 생성된 `conversations` 연관관계는 해당 모델의 타입과 기본 키로 범위가 지정된 다형성 연관관계입니다. 역방향 연관관계를 통해 대화를 소유한 participant에도 접근할 수 있습니다:

```php
$conversations = $team->conversations;

$participant = $conversation->participant;
```

<!-- If your application uses multiple participant model types, you should consider defining an [Eloquent morph map](/docs/13.x/eloquent-relationships#custom-polymorphic-types) so that stored participant types are not coupled to your model class names. -->
애플리케이션에서 여러 참여자 모델 타입을 사용한다면, 저장된 참여자 타입이 모델 클래스 이름에 종속되지 않도록 [Eloquent morph map](/docs/13.x/eloquent-relationships#custom-polymorphic-types)을 정의하는 것이 좋습니다.

> [!WARNING]
> `continue` 및 `continueOrStart` 메서드는 지정된 participant가 대화를 소유하고 있는지 확인하지 않습니다. 대화를 계속하기 전에 애플리케이션에서 해당 대화에 대한 접근 권한을 인가해야 합니다.

<a name="inspecting-stored-conversations"></a>
<!-- #### Inspecting Stored Conversations -->
#### Inspecting Stored Conversations

<!-- When displaying a conversation to your users, you often need details such as message IDs, timestamps, and tool calls. You may resolve the conversation store from the service container to read the stored messages without querying the AI SDK's tables directly: -->
사용자에게 대화를 표시할 때는 메시지 ID, 타임스탬프, 툴 호출과 같은 세부 정보가 필요한 경우가 많습니다. AI SDK의 테이블을 직접 조회하지 않고 저장된 메시지를 읽으려면 서비스 컨테이너에서 대화 저장소를 확인할 수 있습니다.

```php
use Laravel\Ai\Contracts\ConversationStore;

$store = app(ConversationStore::class);
```

<!-- Messages are paginated newest first using a cursor and are returned as `StoredMessage` instances, which contain each message's ID, timestamps, usage, metadata, and attachments: -->
메시지는 커서를 사용해 최신순으로 페이지네이션되며, 각 메시지의 ID, 타임스탬프, 사용량, 메타데이터 및 첨부 파일을 포함하는 `StoredMessage` 인스턴스로 반환됩니다:

```php
$messages = $store->paginateConversationMessages($conversationId, perPage: 25);

foreach ($messages as $message) {
    $message->id;
    $message->role;
    $message->content;
    $message->createdAt;
    $message->usage;
    $message->status;
}
```

<!-- Each turn, which consists of a user prompt and the assistant's reply, is stored as a list of steps. A step is a single request to the provider, so a turn in which the model calls tools will contain several steps. Each tool result is recorded on the tool call that produced it. The `toolCalls`, `providerToolCalls`, and `toolResults` methods flatten these steps in order, so you do not need to traverse them yourself: -->
각 턴은 사용자 프롬프트와 어시스턴트의 응답으로 구성되며, 단계 목록으로 저장됩니다. 단계는 provider에 대한 단일 요청이므로, 모델이 도구를 호출하는 턴에는 여러 단계가 포함됩니다. 각 도구 결과는 해당 결과를 생성한 도구 호출에 기록됩니다. `toolCalls`, `providerToolCalls`, `toolResults` 메서드는 이러한 단계를 순서대로 평탄화하므로, 직접 순회할 필요가 없습니다:

```php
$message->steps;

$message->toolCalls();
$message->providerToolCalls();
$message->toolResults();
```

<!-- A tool call contains a `result` once it has been executed. Tool calls that contain an `approval_reason` but no `result` are still awaiting a [tool approval](#human-tool-approval). -->
도구 호출은 실행되면 `result`를 포함합니다. `approval_reason`은 포함하지만 `result`는 포함하지 않는 도구 호출은 아직 [tool approval](#human-tool-approval)을 기다리고 있습니다.

<!-- The `status` property contains a `Laravel\Ai\Enums\MessageStatus` instance. A turn that failed partway through is stored as `Failed` along with the steps it had already completed, so tool calls that ran before the failure remain in the history. When the conversation continues, any tool call without a recorded result is sent to the model marked as interrupted, since Laravel cannot determine whether it ran. -->
`status` 프로퍼티에는 `Laravel\Ai\Enums\MessageStatus` 인스턴스가 포함됩니다. 중간에 실패한 턴은 이미 완료한 단계와 함께 `Failed`로 저장되므로, 실패 전에 실행된 툴 호출은 기록에 남습니다. 대화가 계속되면 결과가 기록되지 않은 툴 호출은 중단된 것으로 표시되어 모델에 전송됩니다. Laravel은 해당 호출이 실행되었는지 확인할 수 없기 때문입니다.

<!-- Before continuing a conversation via an ID provided by your application's frontend, you should verify that the conversation was stored for the given participant: -->
애플리케이션의 프런트엔드에서 제공한 ID로 대화를 계속하기 전에, 해당 참가자에 대한 대화가 저장되었는지 확인해야 합니다:

```php
abort_unless($store->conversationBelongsTo(
    $conversationId, $user->getMorphClass(), $user->getKey()
), 403);
```

<!-- If the most recent turn is paused awaiting [tool approval](#human-tool-approval), you may render its pending tool calls after a page reload without resuming the run: -->
가장 최근 턴이 [tool approval](#human-tool-approval)을 기다리며 일시 중지된 경우, 실행을 재개하지 않고 페이지를 새로 고친 후 보류 중인 도구 호출을 렌더링할 수 있습니다:

```php
foreach ($store->pendingApprovalsFor($conversationId) as $approval) {
    // $approval->id, $approval->tool, $approval->arguments, $approval->reason...
}
```

<!-- These methods are defined by the `PaginatesConversations`, `VerifiesConversationOwnership`, and `ResolvesPendingApprovals` contracts. The included database store implements all three, while a custom store may implement only the contracts it needs. -->
이 메서드들은 `PaginatesConversations`, `VerifiesConversationOwnership`, `ResolvesPendingApprovals` 컨트랙트에 정의되어 있습니다. 포함된 데이터베이스 스토어는 세 컨트랙트를 모두 구현하지만, 사용자 지정 스토어는 필요한 컨트랙트만 구현할 수 있습니다.

<a name="structured-output"></a>
<!-- ### Structured Output -->
### Structured Output

<!-- If you would like your agent to return structured output, implement the `HasStructuredOutput` interface, which requires that your agent define a `schema` method: -->
에이전트가 구조화된 출력을 반환하도록 하려면 `HasStructuredOutput` 인터페이스를 구현합니다. 이 인터페이스는 에이전트가 `schema` 메서드를 정의하도록 요구합니다.

```php
<?php

namespace App\Ai\Agents;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasStructuredOutput;
use Laravel\Ai\Promptable;

class SalesCoach implements Agent, HasStructuredOutput
{
    use Promptable;

    // ...

    /**
     * Get the agent's structured output schema definition.
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'score' => $schema->integer()->required(),
        ];
    }
}
```

<!-- When prompting an agent that returns structured output, you can access the returned `StructuredAgentResponse` like an array: -->
구조화된 출력을 반환하는 에이전트에 프롬프트할 때는 반환된 `StructuredAgentResponse`를 배열처럼 접근할 수 있습니다.

```php
$response = (new SalesCoach)->prompt('Analyze this sales transcript...');

return $response['score'];
```

<a name="structured-output-nested-objects"></a>
<!-- #### Nested Objects -->
#### Nested Objects

<!-- To define nested structured output, use the `object` method with a closure: -->
중첩된 구조화된 출력을 정의하려면 클로저와 함께 `object` 메서드를 사용합니다.

```php
<?php

namespace App\Ai\Agents;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasStructuredOutput;
use Laravel\Ai\Promptable;

class SalesCoach implements Agent, HasStructuredOutput
{
    use Promptable;

    // ...

    /**
     * Get the agent's structured output schema definition.
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'score' => $schema->integer()->required(),
            'metadata' => $schema->object(fn ($schema) => [
                'confidence' => $schema->string()->enum(['low', 'medium', 'high'])->required(),
                'language' => $schema->string()->required(),
            ])->required(),
        ];
    }
}
```

<a name="structured-output-arrays-of-objects"></a>
<!-- #### Arrays of Objects -->
#### Arrays of Objects

<!-- If your agent should return a list of structured items, combine the `array` and `object` methods: -->
에이전트가 구조화된 항목 목록을 반환해야 한다면, `array`와 `object` 메서드를 함께 사용합니다.

```php
public function schema(JsonSchema $schema): array
{
    return [
        'feedback' => $schema->array()
            ->items(
                $schema->object(fn ($schema) => [
                    'comment' => $schema->string()->required(),
                    'score' => $schema->integer()->required(),
                ])
            )
            ->required(),
    ];
}
```

<!-- If a value may match one of several schemas, use the `anyOf` method: -->
값이 여러 스키마 중 하나와 일치할 수 있다면 `anyOf` 메서드를 사용합니다.

```php
public function schema(JsonSchema $schema): array
{
    return [
        'content' => $schema->anyOf([
            $schema->object(fn ($schema) => [
                'type' => $schema->string()->enum(['article'])->required(),
                'title' => $schema->string()->required(),
            ]),
            $schema->object(fn ($schema) => [
                'type' => $schema->string()->enum(['image'])->required(),
                'url' => $schema->string()->required(),
            ]),
        ])->required(),
    ];
}
```

<a name="attachments"></a>
<!-- ### Attachments -->
### Attachments

<!-- When prompting, you may also pass attachments with the prompt to allow the model to inspect images and documents: -->
프롬프트를 보낼 때, 모델이 이미지와 문서를 살펴볼 수 있도록 프롬프트와 함께 첨부 파일을 전달할 수도 있습니다.

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Files;

$response = (new SalesCoach)->prompt(
    'Analyze the attached sales transcript...',
    attachments: [
        Files\Document::fromStorage('transcript.pdf'), // Attach a document from a filesystem disk...
        Files\Document::fromPath('/home/laravel/transcript.md'), // Attach a document from a local path...
        $request->file('transcript'), // Attach an uploaded file...
    ]
);
```

<!-- Likewise, the `Laravel\Ai\Files\Image` class may be used to attach images to a prompt: -->
마찬가지로, `Laravel\Ai\Files\Image` 클래스를 사용하여 프롬프트에 이미지를 첨부할 수 있습니다.

```php
use App\Ai\Agents\ImageAnalyzer;
use Laravel\Ai\Files;

$response = (new ImageAnalyzer)->prompt(
    'What is in this image?',
    attachments: [
        Files\Image::fromStorage('photo.jpg'), // Attach an image from a filesystem disk...
        Files\Image::fromPath('/home/laravel/photo.jpg'), // Attach an image from a local path...
        $request->file('photo'), // Attach an uploaded file...
    ]
);
```

<a name="streaming"></a>
<!-- ### Streaming -->
### Streaming

<!-- You may stream an agent's response by invoking the `stream` method. The returned `StreamableAgentResponse` may be returned from a route to automatically send a streaming response (SSE) to the client: -->
`stream` 메서드를 호출하여 에이전트의 응답을 스트리밍할 수 있습니다. 반환되는 `StreamableAgentResponse`는 라우트에서 그대로 반환할 수 있으며, 그러면 클라이언트에 스트리밍 응답(SSE)이 자동으로 전송됩니다.

```php
use App\Ai\Agents\SalesCoach;

Route::get('/coach', function () {
    return (new SalesCoach)->stream('Analyze this sales transcript...');
});
```

<!-- The `then` method may be used to provide a closure that will be invoked when the entire response has been streamed to the client: -->
`then` 메서드를 사용하면 전체 응답이 클라이언트에 스트리밍된 뒤 호출될 클로저를 제공할 수 있습니다.

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Responses\StreamedAgentResponse;

Route::get('/coach', function () {
    return (new SalesCoach)
        ->stream('Analyze this sales transcript...')
        ->then(function (StreamedAgentResponse $response) {
            // $response->text, $response->events, $response->usage...
        });
});
```

<!-- Alternatively, you may iterate through the streamed events manually: -->
또는 스트리밍된 이벤트를 직접 순회할 수도 있습니다.

```php
$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

foreach ($stream as $event) {
    // ...
}
```

<!-- The response also contains the model's reasoning and any sources it cited. Both are stored with the assistant message when using the `RemembersConversations` trait: -->
응답에는 모델의 추론과 모델이 인용한 출처도 포함됩니다. `RemembersConversations` 트레이트를 사용할 때는 둘 다 어시스턴트 메시지와 함께 저장됩니다.

```php
use Laravel\Ai\Responses\StreamedAgentResponse;

(new SalesCoach)
    ->stream('Analyze this sales transcript...')
    ->then(function (StreamedAgentResponse $response) {
        $response->reasoning; // '' unless the model returned reasoning text...
        $response->meta->citations;
    });
```

<!-- Reasoning is also available on responses returned by the `prompt` method. -->
`prompt` 메서드가 반환하는 응답에는 추론도 포함됩니다.

<a name="streaming-using-the-vercel-ai-sdk-protocol"></a>
<a name="stream-protocols"></a>
<!-- #### Stream Protocols -->
#### Stream Protocols

<!-- By default, streamed responses use the AI SDK's own event format. However, you may use a frontend streaming protocol instead, which allows you to pair your agent with an existing chat interface rather than building your own. -->
기본적으로 스트리밍 응답은 AI SDK 자체의 이벤트 형식을 사용합니다. 하지만 대신 프론트엔드 스트리밍 프로토콜을 사용할 수도 있으며, 이를 통해 직접 채팅 인터페이스를 구축하는 대신 에이전트를 기존 채팅 인터페이스와 연동할 수 있습니다.

<!-- You may stream the events using the [Vercel AI SDK stream protocol](https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocol) by invoking the `usingVercelDataProtocol` method on the streamable response: -->
스트리밍 가능한 응답에서 `usingVercelDataProtocol` 메서드를 호출하여 [Vercel AI SDK stream protocol](https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocol)을 사용해 이벤트를 스트리밍할 수 있습니다.

```php
use App\Ai\Agents\SalesCoach;

Route::get('/coach', function () {
    return (new SalesCoach)
        ->stream('Analyze this sales transcript...')
        ->usingVercelDataProtocol();
});
```

<!-- You may pass a message ID if your application's frontend assigns its own: -->
애플리케이션의 프런트엔드에서 자체 메시지 ID를 할당한다면 해당 ID를 전달할 수 있습니다:

```php
->usingVercelDataProtocol($request->string('messageId'));
```

<!-- Alternatively, the `usingAgentUserInteractionProtocol` method may be used to stream using the [Agent User Interaction (AG-UI) protocol](https://docs.ag-ui.com): -->
또는 [Agent User Interaction (AG-UI) protocol](https://docs.ag-ui.com)을 사용해 스트리밍하려면 `usingAgentUserInteractionProtocol` 메서드를 사용할 수 있습니다.

```php
Route::post('/coach', function (Request $request) {
    return (new SalesCoach)
        ->forUser($request->user())
        ->stream($request->string('prompt'))
        ->usingAgentUserInteractionProtocol();
});
```

<!-- The `threadId` and `runId` arguments are optional and default to the conversation ID and the invocation ID: -->
`threadId` 및 `runId` 인수는 선택 사항이며, 기본값은 대화 ID와 호출 ID입니다:

```php
->usingAgentUserInteractionProtocol(
    threadId: $request->input('threadId'),
    runId: $request->input('runId'),
);
```

<!-- To use a protocol that the AI SDK does not implement, you may pass your own `Laravel\Ai\Streaming\Protocols\StreamProtocol` implementation to the `usingProtocol` method: -->
AI SDK에서 구현하지 않는 프로토콜을 사용하려면 `usingProtocol` 메서드에 직접 만든 `Laravel\Ai\Streaming\Protocols\StreamProtocol` 구현을 전달할 수 있습니다:

```php
use App\Ai\Protocols\CustomProtocol;

return (new SalesCoach)
    ->stream('Analyze this sales transcript...')
    ->usingProtocol(new CustomProtocol);
```

<a name="chat-requests"></a>
<a name="frontend-integration"></a>
<!-- #### Frontend Integration -->
#### Frontend Integration

<!-- Chat interfaces built with libraries such as Vercel's `useChat` or CopilotKit already render messages, tool calls, and approval prompts, so your application only needs to handle the requests they send. Each request contains the conversation history, the newest user message, and any tool approval responses. -->
`useChat` 또는 CopilotKit과 같은 라이브러리로 구축된 채팅 인터페이스는 이미 메시지, 툴 호출, 승인 프롬프트를 렌더링하므로 애플리케이션에서는 해당 인터페이스가 보내는 요청만 처리하면 됩니다. 각 요청에는 대화 기록, 가장 최근의 사용자 메시지, 툴 승인 응답이 포함됩니다.

<!-- The `Vercel::chat` and `AgentUserInteraction::chat` methods convert such a request into an object that may be passed directly to an agent's `stream` method: -->
`Vercel::chat` 및 `AgentUserInteraction::chat` 메서드는 이러한 요청을 에이전트의 `stream` 메서드에 직접 전달할 수 있는 객체로 변환합니다:

```php
use Laravel\Ai\Vercel\Vercel;

Route::post('/chat', function (Request $request) {
    $chat = Vercel::chat($request);

    return (new SupportAgent)
        ->withMessages($chat->history())
        ->stream($chat)
        ->usingProtocol($chat->protocol());
});
```

<!-- If the request contains [approval decisions](#human-tool-approval), the agent will resume using those decisions. Otherwise, the agent is prompted with the request's newest user message and attachments. The `protocol` method returns the protocol used by the client. -->
요청에 [approval decisions](#human-tool-approval)이 포함되어 있으면 에이전트는 해당 결정을 사용해 작업을 재개합니다. 그렇지 않으면 요청의 최신 사용자 메시지와 첨부 파일을 바탕으로 에이전트에 프롬프트가 전달됩니다. `protocol` 메서드는 클라이언트가 사용하는 프로토콜을 반환합니다.

> [!NOTE]
> `Conversational` 인터페이스를 구현하는 에이전트는 자체 기록을 로드하므로 `withMessages` 메서드를 생략할 수 있습니다.

<!-- The `AgentUserInteraction::chat` method provides the same API for AG-UI clients, in addition to the request's thread and run IDs: -->
`AgentUserInteraction::chat` 메서드는 요청의 스레드 및 실행 ID와 함께 AG-UI 클라이언트에도 동일한 API를 제공합니다:

```php
use Laravel\Ai\AgentUserInteraction\AgentUserInteraction;

$chat = AgentUserInteraction::chat($request);

$chat->threadId();
$chat->runId();
```

<!-- You may also convert stored messages back into the format a client expects, allowing the client to display a previous conversation, such as after a page reload: -->
저장된 메시지를 클라이언트가 기대하는 형식으로 다시 변환할 수도 있으므로, 페이지를 새로 고친 후처럼 클라이언트가 이전 대화를 표시할 수 있습니다.

```php
$messages = $conversation->messages()->oldest()->get();

return ['messages' => Vercel::toUiMessages($messages)];
```

<!-- The `AgentUserInteraction::toClientState` method performs the same conversion for AG-UI clients, in addition to returning any pending approval interrupts: -->
`AgentUserInteraction::toClientState` 메서드는 AG-UI 클라이언트에 대해 동일한 변환을 수행하며, 대기 중인 승인 인터럽트도 반환합니다:

```php
return AgentUserInteraction::toClientState($messages);
```

<a name="broadcasting"></a>
<!-- ### Broadcasting -->
### Broadcasting

<!-- You may broadcast streamed events in a few different ways. First, you can simply invoke the `broadcast` or `broadcastNow` method on a streamed event: -->
스트리밍된 이벤트는 몇 가지 방식으로 브로드캐스트할 수 있습니다. 먼저, 스트리밍된 이벤트에서 `broadcast` 또는 `broadcastNow` 메서드를 간단히 호출할 수 있습니다.

```php
use App\Ai\Agents\SalesCoach;
use Illuminate\Broadcasting\Channel;

$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

foreach ($stream as $event) {
    $event->broadcast(new Channel('channel-name'));
}
```

<!-- Or, you can invoke an agent's `broadcastOnQueue` method to queue the agent operation and broadcast the streamed events as they are available: -->
또는 에이전트의 `broadcastOnQueue` 메서드를 호출하여 에이전트 작업을 큐에 넣고, 스트리밍된 이벤트가 준비되는 대로 브로드캐스트할 수 있습니다.

```php
(new SalesCoach)->broadcastOnQueue(
    'Analyze this sales transcript...',
    new Channel('channel-name'),
);
```

<a name="skipping-oversized-events"></a>
<!-- #### Skipping Oversized Events -->
#### Skipping Oversized Events

<!-- Some broadcasting platforms limit WebSocket messages to around 10KB. Data-heavy stream events, like large tool results, can exceed this limit and cause broadcasting to fail. You may exclude specific event types from broadcasting using the `WithoutBroadcasting` attribute: -->
일부 브로드캐스팅 플랫폼은 WebSocket 메시지를 약 10KB로 제한합니다. 큰 도구 결과처럼 데이터가 많은 스트리밍 이벤트는 이 제한을 초과해 브로드캐스팅이 실패할 수 있습니다. `WithoutBroadcasting` 속성을 사용해 특정 이벤트 타입을 브로드캐스팅에서 제외할 수 있습니다:

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Attributes\WithoutBroadcasting;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasTools;
use Laravel\Ai\Promptable;
use Laravel\Ai\Streaming\Events\ToolCall;
use Laravel\Ai\Streaming\Events\ToolResult;

#[WithoutBroadcasting(ToolCall::class, ToolResult::class)]
class SearchAgent implements Agent, HasTools
{
    use Promptable;

    // ...
}
```

<!-- The excluded events are never broadcast, but they are still persisted to the `agent_conversation_messages` table, so your frontend can load the full tool data after the stream completes. This works for both queued (`broadcastOnQueue`) and synchronous (`broadcast` / `broadcastNow`) broadcasting. -->
제외된 이벤트는 절대 브로드캐스트되지 않지만, `agent_conversation_messages` 테이블에는 계속 저장되므로 스트림이 완료된 뒤 프런트엔드에서 전체 도구 데이터를 불러올 수 있습니다. 이는 큐 기반(`broadcastOnQueue`) 브로드캐스팅과 동기식(`broadcast` / `broadcastNow`) 브로드캐스팅 모두에서 동작합니다.

<a name="queueing"></a>
<!-- ### Queueing -->
### Queueing

<!-- Using an agent's `queue` method, you may prompt the agent, but allow it to process the response in the background, keeping your application feeling fast and responsive. The `then` and `catch` methods may be used to register closures that will be invoked when a response is available or if an exception occurs: -->
에이전트의 `queue` 메서드를 사용하면 에이전트에 프롬프트를 보내되, 응답 처리는 백그라운드에서 수행하도록 할 수 있습니다. 이렇게 하면 애플리케이션을 빠르고 반응성 있게 유지할 수 있습니다. `then`과 `catch` 메서드를 사용하여 응답을 사용할 수 있게 되었을 때 또는 예외가 발생했을 때 호출될 클로저를 등록할 수 있습니다.

```php
use Illuminate\Http\Request;
use Laravel\Ai\Responses\AgentResponse;
use Throwable;

Route::post('/coach', function (Request $request) {
    (new SalesCoach)
        ->queue($request->input('transcript'))
        ->then(function (AgentResponse $response) {
            // ...
        })
        ->catch(function (Throwable $e) {
            // ...
        });

    return back();
});
```

<a name="tools"></a>
<!-- ### Tools -->
### Tools

<!-- Tools may be used to give agents additional functionality that they can utilize while responding to prompts. Tools can be created using the `make:tool` Artisan command: -->
도구는 에이전트가 프롬프트에 응답하는 동안 활용할 수 있는 추가 기능을 제공하는 데 사용됩니다. 도구는 `make:tool` Artisan 명령어를 사용하여 만들 수 있습니다.

```shell
php artisan make:tool RandomNumberGenerator
```

<!-- The generated tool will be placed in your application's `app/Ai/Tools` directory. Each tool contains a `handle` method that will be invoked by the agent when it needs to utilize the tool: -->
생성된 도구는 애플리케이션의 `app/Ai/Tools` 디렉터리에 배치됩니다. 각 도구에는 에이전트가 해당 도구를 사용해야 할 때 호출되는 `handle` 메서드가 포함됩니다.

```php
<?php

namespace App\Ai\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Ai\Contracts\Tool;
use Laravel\Ai\Tools\Request;
use Stringable;

class RandomNumberGenerator implements Tool
{
    /**
     * Get the description of the tool's purpose.
     */
    public function description(): Stringable|string
    {
        return 'This tool may be used to generate cryptographically secure random numbers.';
    }

    /**
     * Execute the tool.
     */
    public function handle(Request $request): Stringable|string
    {
        return (string) random_int($request['min'], $request['max']);
    }

    /**
     * Get the tool's schema definition.
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'min' => $schema->integer()->min(0)->required(),
            'max' => $schema->integer()->required(),
        ];
    }
}
```

<!-- Once you have defined your tool, you may return it from the `tools` method of any of your agents: -->
도구를 정의한 뒤에는 에이전트의 `tools` 메서드에서 해당 도구를 반환할 수 있습니다.

```php
use App\Ai\Tools\RandomNumberGenerator;

/**
 * Get the tools available to the agent.
 *
 * @return Tool[]
 */
public function tools(): iterable
{
    return [
        new RandomNumberGenerator,
    ];
}
```

<a name="runtime-tool-overrides"></a>
<!-- #### Runtime Tool Overrides -->
#### Runtime Tool Overrides

<!-- The `withTools` method may be used to replace the tools declared by an agent instance. This is useful for per-tenant or feature-flagged tool sets: -->
`withTools` 메서드를 사용하면 에이전트 인스턴스에 선언된 도구를 교체할 수 있습니다. 이는 테넌트별 또는 기능 플래그가 적용된 도구 세트에 유용합니다:

```php
$response = (new SupportAgent)
    ->withTools([new LookupOrder])
    ->prompt('Where is order 12345?');
```

<!-- You may also pass a closure, which receives the agent's declared tools, allowing you to append to or filter them: -->
클로저를 전달할 수도 있습니다. 이 클로저는 에이전트가 선언한 툴을 전달받으므로, 툴을 추가하거나 필터링할 수 있습니다.

```php
$response = (new SupportAgent)
    ->withTools(fn (array $tools) => [...$tools, new LookupOrder])
    ->prompt('Where is order 12345?');
```

<a name="validating-tool-arguments"></a>
<!-- #### Validating Tool Arguments -->
#### Validating Tool Arguments

<!-- Although your tool's schema constrains the arguments a model may provide, you may validate the incoming arguments using the request's `validate` method: -->
툴의 스키마가 모델이 제공할 수 있는 인수를 제한하더라도, 요청의 `validate` 메서드를 사용해 들어오는 인수의 유효성을 검증할 수 있습니다:

```php
public function handle(Request $request): Stringable|string
{
    $validated = $request->validate([
        'city' => 'required|string',
        'days' => 'required|integer|max:7',
    ]);

    return $this->forecast($validated['city'], $validated['days']);
}
```

<!-- When validation fails, the validation messages are returned to the model as the tool's result, allowing it to correct the arguments and call the tool again. -->
유효성 검증에 실패하면 유효성 검증 메시지가 툴의 결과로 모델에 반환되므로, 모델은 인수를 수정하고 툴을 다시 호출할 수 있습니다.

<a name="repairing-tool-calls"></a>
<!-- #### Repairing Tool Calls -->
#### Repairing Tool Calls

<!-- Use the `RepairToolCalls` attribute to let an agent recover when a model calls an unknown local tool. Laravel returns the failed call to the model with the names of the available local tools, allowing it to correct the call: -->
`RepairToolCalls` 속성을 사용하면 모델이 알 수 없는 로컬 툴을 호출했을 때 에이전트가 복구하도록 할 수 있습니다. Laravel은 사용 가능한 로컬 툴의 이름과 함께 실패한 호출을 모델에 반환하므로, 모델이 호출을 수정할 수 있습니다:

```php
use Laravel\Ai\Attributes\RepairToolCalls;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasTools;
use Laravel\Ai\Promptable;

#[RepairToolCalls]
class SupportAgent implements Agent, HasTools
{
    use Promptable;

    // ...
}
```

<!-- When Laravel derives the maximum number of steps automatically, this attribute adds one step for the repaired call. Explicit `MaxSteps` limits are unchanged. -->
Laravel이 최대 단계 수를 자동으로 계산할 때 이 속성은 복구된 호출을 위해 단계 하나를 추가합니다. 명시적으로 지정한 `MaxSteps` 제한은 변경되지 않습니다.

<a name="similarity-search"></a>
<!-- #### Similarity Search -->
#### Similarity Search

<!-- The `SimilaritySearch` tool allows agents to search for documents similar to a given query using vector embeddings stored in your database. This is useful for retrieval-augmented generation (RAG) when you want to give agents access to search your application's data. -->
`SimilaritySearch` 도구를 사용하면 에이전트가 데이터베이스에 저장된 벡터 임베딩을 사용하여 주어진 쿼리와 유사한 문서를 검색할 수 있습니다. 이는 에이전트가 애플리케이션 데이터에 접근하여 검색할 수 있게 하려는 경우, 검색 증강 생성(RAG)에 유용합니다.

<!-- The simplest way to create a similarity search tool is using the `usingModel` method with an Eloquent model that has vector embeddings: -->
유사도 검색 도구를 만드는 가장 간단한 방법은 벡터 임베딩을 가진 Eloquent 모델과 함께 `usingModel` 메서드를 사용하는 것입니다.

```php
use App\Models\Document;
use Laravel\Ai\Tools\SimilaritySearch;

public function tools(): iterable
{
    return [
        SimilaritySearch::usingModel(Document::class, 'embedding'),
    ];
}
```

<!-- The first argument is the Eloquent model class, and the second argument is the column containing the vector embeddings. -->
첫 번째 인수는 Eloquent 모델 클래스이고, 두 번째 인수는 벡터 임베딩을 포함하는 컬럼입니다.

<!-- You may also provide a minimum similarity threshold between `0.0` and `1.0` and a closure to customize the query: -->
`0.0`에서 `1.0` 사이의 최소 유사도 임계값과 쿼리를 사용자 정의하기 위한 클로저도 제공할 수 있습니다.

```php
SimilaritySearch::usingModel(
    model: Document::class,
    column: 'embedding',
    minSimilarity: 0.7,
    limit: 10,
    query: fn ($query) => $query->where('published', true),
),
```

<!-- For more control, you may create a similarity search tool with a custom closure that returns the search results: -->
더 세밀하게 제어하려면, 검색 결과를 반환하는 사용자 정의 클로저로 유사도 검색 도구를 만들 수 있습니다.

```php
use App\Models\Document;
use Laravel\Ai\Tools\SimilaritySearch;

public function tools(): iterable
{
    return [
        new SimilaritySearch(using: function (string $query) {
            return Document::query()
                ->where('user_id', $this->user->id)
                ->whereVectorSimilarTo('embedding', $query)
                ->limit(10)
                ->get();
        }),
    ];
}
```

<!-- You may customize the tool's description using the `withDescription` method: -->
`withDescription` 메서드를 사용하여 도구의 설명을 사용자 정의할 수 있습니다.

```php
SimilaritySearch::usingModel(Document::class, 'embedding')
    ->withDescription('Search the knowledge base for relevant articles.'),
```

<a name="deferred-tool-loading"></a>
<!-- ### Deferred Tool Loading -->
### Deferred Tool Loading

<!-- By default, every tool an agent exposes is sent to the provider with each request. When an agent provides a large number of tools, this consumes tokens and may reduce the accuracy of the model's tool selection. Using the `ToolSearch` provider tool with OpenAI or Anthropic, you may defer tool definitions so that the provider only loads them when they are needed: -->
기본적으로 에이전트가 제공하는 모든 툴은 각 요청과 함께 프로바이더로 전송됩니다. 에이전트가 많은 수의 툴을 제공하면 토큰을 소모하고 모델의 툴 선택 정확도가 낮아질 수 있습니다. OpenAI 또는 Anthropic에서 `ToolSearch` 프로바이더 툴을 사용하면 툴 정의를 지연시켜 프로바이더가 필요한 경우에만 해당 정의를 로드하도록 할 수 있습니다:

```php
use App\Ai\Tools\RefundOrder;
use App\Ai\Tools\SearchInvoices;
use App\Ai\Tools\Weather;
use Laravel\Ai\Providers\Tools\ToolSearch;

public function tools(): iterable
{
    return [
        new Weather,
        new ToolSearch(tools: [
            new SearchInvoices,
            new RefundOrder,
        ]),
    ];
}
```

<!-- The wrapped tools do not require any modification. The provider will search for and load them when they are relevant to the prompt, after which the agent may call them like any other tool. -->
래핑된 툴은 수정할 필요가 없습니다. 프로바이더는 프롬프트와 관련된 툴을 검색하고 로드하며, 이후 에이전트는 다른 툴과 마찬가지로 해당 툴을 호출할 수 있습니다.

<!-- When using Anthropic, the `strategy` argument may be used to determine how the provider should search for deferred tools. The supported strategies are `regex` (default) and `bm25`: -->
Anthropic을 사용할 때 `strategy` 인수로 프로바이더가 지연된 툴을 검색하는 방식을 결정할 수 있습니다. 지원되는 전략은 `regex`(기본값)와 `bm25`입니다.

```php
new ToolSearch(tools: [new SearchInvoices], strategy: 'bm25'),
```

<!-- When using Anthropic, additional provider-specific options may be passed to the search tool using the `withProviderOptions` method: -->
Anthropic을 사용할 때는 `withProviderOptions` 메서드를 사용해 검색 툴에 프로바이더별 옵션을 추가로 전달할 수 있습니다.

```php
(new ToolSearch(tools: [new SearchInvoices]))
    ->withProviderOptions(['cache_control' => ['type' => 'ephemeral']]),
```

> [!WARNING]
> 도구 검색을 지원하지 않는 프로바이더는 지연된 툴을 조용히 삭제하는 대신 예외를 발생시킵니다. 또한 Anthropic은 `ToolSearch` 래퍼 외부에 하나 이상의 툴이 제공되어야 합니다.

<a name="file-storage-tools"></a>
<!-- ### File Storage Tools -->
### File Storage Tools

<!-- The `FileStorage` tool factory allows you to give agents access to a Laravel [filesystem disk](/docs/13.x/filesystem). The `all` method returns tools that allow the agent to list, read, inspect, generate URLs for, write, delete, and copy files on the given disk: -->
`FileStorage` 툴 팩토리를 사용하면 에이전트에 Laravel [filesystem disk](/docs/13.x/filesystem)에 대한 액세스 권한을 부여할 수 있습니다. `all` 메서드는 에이전트가 지정한 디스크의 파일을 나열하고, 읽고, 검사하고, URL을 생성하고, 쓰고, 삭제하고, 복사할 수 있는 툴을 반환합니다:

```php
use Laravel\Ai\Tools\FileStorage;

public function tools(): iterable
{
    return FileStorage::all('local');
}
```

<!-- If your agent should only be able to inspect files, use the `readOnly` method: -->
에이전트가 파일을 검사만 할 수 있어야 한다면 `readOnly` 메서드를 사용하세요:

```php
return FileStorage::readOnly('local');
```

<!-- These methods return an `Illuminate\Support\Collection`, allowing you to further filter the tools that are provided to the agent: -->
이 메서드들은 `Illuminate\Support\Collection`을 반환하므로, 에이전트에 제공되는 툴을 추가로 필터링할 수 있습니다:

```php
use Laravel\Ai\Tools\Filesystem\DeleteFile;

return FileStorage::all('s3')
    ->reject(fn ($tool) => $tool instanceof DeleteFile);
```

<a name="mcp-tools"></a>
<!-- ### MCP Tools -->
### MCP Tools

<!-- If your application uses [Laravel MCP](/docs/13.x/mcp), you may give your agents tools exposed by [Model Context Protocol](https://modelcontextprotocol.io) servers. Using the [Laravel MCP client](/docs/13.x/mcp#client), you may connect to a remote or local MCP server and pass its tools directly to your agent. -->
애플리케이션에서 [Laravel MCP](/docs/13.x/mcp)를 사용하는 경우, [Model Context Protocol](https://modelcontextprotocol.io) 서버가 제공하는 툴을 에이전트에 제공할 수 있습니다. [Laravel MCP client](/docs/13.x/mcp#client)를 사용하면 원격 또는 로컬 MCP 서버에 연결하고 해당 서버의 툴을 에이전트에 직접 전달할 수 있습니다.

> [!NOTE]
> MCP 도구를 사용하려면 애플리케이션에 [Laravel MCP](/docs/13.x/mcp) 패키지를 설치해야 합니다.

<!-- Because an MCP client's `tools` method returns a collection, spread it into your agent's `tools` array using the `...` operator: -->
MCP 클라이언트의 `tools` 메서드는 컬렉션을 반환하므로, `...` 연산자를 사용하여 에이전트의 `tools` 배열에 펼쳐 넣습니다.

```php
use App\Ai\Tools\RandomNumberGenerator;
use Laravel\Mcp\Client;

/**
 * Get the tools available to the agent.
 *
 * @return Tool[]
 */
public function tools(): iterable
{
    return [
        ...Client::web('https://mcp.example.com')
            ->withToken($token)
            ->tools(),

        new RandomNumberGenerator,
    ];
}
```

<!-- The AI SDK automatically wraps each MCP tool so the agent can call it like any other tool. You may also use a [named MCP client](/docs/13.x/mcp#named-clients): -->
AI SDK는 각 MCP 툴을 자동으로 래핑하므로 에이전트가 다른 툴과 마찬가지로 호출할 수 있습니다. [named MCP client](/docs/13.x/mcp#named-clients)를 사용할 수도 있습니다:

```php
use Laravel\Mcp\Facades\Mcp;

public function tools(): iterable
{
    return [
        ...Mcp::client('github')->tools(),
    ];
}
```

<!-- Or connect to a [local MCP server](/docs/13.x/mcp#client-connecting): -->
또는 [local MCP server](/docs/13.x/mcp#client-connecting)에 연결합니다:

```php
use Laravel\Mcp\Client;

public function tools(): iterable
{
    return [
        ...Client::local('php', ['artisan', 'mcp:start'])->tools(),
    ];
}
```

<!-- For more information on creating and authenticating MCP clients, including bearer tokens and OAuth, consult the [MCP client documentation](/docs/13.x/mcp#client). -->
MCP 클라이언트 생성 및 인증과 bearer 토큰, OAuth에 대한 자세한 내용은 [MCP client documentation](/docs/13.x/mcp#client)를 참고하세요.

<a name="provider-tools"></a>
<!-- ### Provider Tools -->
### Provider Tools

<!-- Provider tools are special tools implemented natively by AI providers, offering capabilities like web searching, URL fetching, and file searching. Unlike regular tools, provider tools are executed by the provider itself rather than your application. -->
제공자 도구는 AI 제공자가 기본적으로 구현한 특별한 도구로, 웹 검색, URL 가져오기, 파일 검색과 같은 기능을 제공합니다. 일반 도구와 달리 제공자 도구는 애플리케이션이 아니라 제공자 자체에서 실행됩니다.

<!-- Provider tools can be returned by your agent's `tools` method. -->
제공자 도구는 에이전트의 `tools` 메서드에서 반환할 수 있습니다.

<a name="web-search"></a>
<!-- #### Web Search -->
#### Web Search

<!-- The `WebSearch` provider tool allows agents to search the web for real-time information. This is useful for answering questions about current events, recent data, or topics that may have changed since the model's training cutoff. -->
`WebSearch` 제공자 도구를 사용하면 에이전트가 실시간 정보를 얻기 위해 웹을 검색할 수 있습니다. 모델의 학습 기준 시점 이후 변경되었을 수 있는 최신 사건, 최근 데이터, 또는 주제에 관한 질문에 답할 때 유용합니다.

<!-- **Supported providers:** Anthropic, OpenAI, Azure, Gemini, xAI, OpenRouter -->
**지원되는 프로바이더:** Anthropic, OpenAI, Azure, Gemini, xAI, OpenRouter

```php
use Laravel\Ai\Providers\Tools\WebSearch;

public function tools(): iterable
{
    return [
        new WebSearch,
    ];
}
```

<!-- You may configure the web search tool to limit the number of searches or restrict results to specific domains: -->
웹 검색 도구는 검색 횟수를 제한하거나 결과를 특정 도메인으로 제한하도록 설정할 수 있습니다.

```php
(new WebSearch)->max(5)->allow(['laravel.com', 'php.net']),
```

<!-- To refine search results based on user location, use the `location` method: -->
사용자 위치를 기준으로 검색 결과를 더 정교하게 조정하려면 `location` 메서드를 사용합니다.

```php
(new WebSearch)->location(
    city: 'New York',
    region: 'NY',
    country: 'US'
);
```

<a name="web-fetch"></a>
<!-- #### Web Fetch -->
#### Web Fetch

<!-- The `WebFetch` provider tool allows agents to fetch and read the contents of web pages. This is useful when you need the agent to analyze specific URLs or retrieve detailed information from known web pages. -->
`WebFetch` 제공자 도구를 사용하면 에이전트가 웹 페이지의 내용을 가져와 읽을 수 있습니다. 에이전트가 특정 URL을 분석하거나 알려진 웹 페이지에서 자세한 정보를 가져와야 할 때 유용합니다.

<!-- **Supported providers:** Anthropic, Gemini, OpenRouter -->
**지원되는 프로바이더:** Anthropic, Gemini, OpenRouter

```php
use Laravel\Ai\Providers\Tools\WebFetch;

public function tools(): iterable
{
    return [
        new WebFetch,
    ];
}
```

<!-- You may configure the web fetch tool to limit the number of fetches or restrict to specific domains: -->
웹 가져오기 도구는 가져오기 횟수를 제한하거나 특정 도메인으로 제한하도록 설정할 수 있습니다.

```php
(new WebFetch)->max(3)->allow(['docs.laravel.com']),
```

<a name="file-search"></a>
<!-- #### File Search -->
#### File Search

<!-- The `FileSearch` provider tool allows agents to search through [files](#files) stored in [vector stores](#vector-stores). This enables retrieval-augmented generation (RAG) by allowing the agent to search your uploaded documents for relevant information. -->
`FileSearch` 제공자 도구를 사용하면 에이전트가 [files](#files)에 저장된 [vector stores](#vector-stores)를 검색할 수 있습니다. 이를 통해 에이전트가 업로드된 문서에서 관련 정보를 검색할 수 있으므로 검색 증강 생성(RAG)을 사용할 수 있습니다.

<!-- **Supported providers:** OpenAI, Gemini, xAI -->
**지원되는 프로바이더:** OpenAI, Gemini, xAI

```php
use Laravel\Ai\Providers\Tools\FileSearch;

public function tools(): iterable
{
    return [
        new FileSearch(stores: ['store_id']),
    ];
}
```

<!-- You may provide multiple vector store IDs to search across multiple stores: -->
여러 저장소를 대상으로 검색하려면 여러 vector store ID를 제공할 수 있습니다.

```php
new FileSearch(stores: ['store_1', 'store_2']);
```

<!-- If your files have [metadata](#adding-files-to-stores), you may filter the search results by providing a `where` argument. For simple equality filters, pass an array: -->
파일에 [metadata](#adding-files-to-stores)가 있다면, `where` 인수를 제공하여 검색 결과를 필터링할 수 있습니다. 단순 동등 조건 필터에는 배열을 전달합니다.

```php
new FileSearch(stores: ['store_id'], where: [
    'author' => 'Taylor Otwell',
    'year' => 2026,
]);
```

<!-- For more complex filters, you may pass a closure that receives a `FileSearchQuery` instance: -->
더 복잡한 필터에는 `FileSearchQuery` 인스턴스를 받는 클로저를 전달할 수 있습니다.

```php
use Laravel\Ai\Providers\Tools\FileSearchQuery;

new FileSearch(stores: ['store_id'], where: fn (FileSearchQuery $query) =>
    $query->where('author', 'Taylor Otwell')
        ->whereNot('status', 'draft')
        ->whereIn('category', ['news', 'updates'])
);
```

<a name="code-execution"></a>
<!-- #### Code Execution -->
#### Code Execution

<!-- The `CodeExecution` provider tool allows agents to run code in a sandbox hosted by the AI provider. This is useful for performing calculations and analyzing data. -->
`CodeExecution` 프로바이더 툴을 사용하면 에이전트가 AI 프로바이더가 호스팅하는 샌드박스에서 코드를 실행할 수 있습니다. 계산을 수행하고 데이터를 분석할 때 유용합니다.

<!-- **Supported providers:** Anthropic, OpenAI, Azure, Gemini, xAI -->
**지원되는 프로바이더:** Anthropic, OpenAI, Azure, Gemini, xAI

```php
use Laravel\Ai\Providers\Tools\CodeExecution;

public function tools(): iterable
{
    return [new CodeExecution];
}
```

<!-- When using OpenAI or Azure, you may make [stored files](#files) available to the sandbox via provider options: -->
OpenAI 또는 Azure를 사용할 때는 프로바이더 옵션을 통해 [stored files](#files)를 샌드박스에서 사용할 수 있도록 설정할 수 있습니다:

```php
(new CodeExecution)->withProviderOptions([
    'container' => ['type' => 'auto', 'file_ids' => ['file_123']],
]);
```

<a name="sub-agents"></a>
<!-- ### Sub-Agents -->
### Sub-Agents

<!-- Agents may also be returned from another agent's `tools` method. When an agent is returned as a tool, the parent agent may delegate a specific task to the sub-agent and use the sub-agent's response while answering the original prompt. This is useful when a general-purpose agent needs access to specialized agents with their own instructions, tools, model configuration, or provider preferences. -->
에이전트는 다른 에이전트의 `tools` 메서드에서 반환될 수도 있습니다. 에이전트가 툴로 반환되면, 부모 에이전트는 특정 작업을 하위 에이전트에 위임하고 원래 프롬프트에 답변하는 동안 하위 에이전트의 응답을 사용할 수 있습니다. 범용 에이전트가 자체 지침, 툴, 모델 설정 또는 프로바이더 선호도를 가진 특화 에이전트에 접근해야 할 때 유용합니다.

<!-- For example, a customer support agent could delegate refund eligibility questions to a dedicated refunds agent: -->
예를 들어 고객 지원 에이전트는 환불 자격 질문을 전담 환불 에이전트에 위임할 수 있습니다:

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasTools;
use Laravel\Ai\Promptable;

class CustomerSupportAgent implements Agent, HasTools
{
    use Promptable;

    /**
     * Get the instructions that the agent should follow.
     */
    public function instructions(): string
    {
        return 'You help customers with account, order, and billing questions. Delegate refund policy questions to the refunds specialist.';
    }

    /**
     * Get the tools available to the agent.
     *
     * @return Tool[]
     */
    public function tools(): iterable
    {
        return [
            new RefundsAgent,
        ];
    }
}
```

<!-- To customize how the sub-agent is exposed to the parent agent, implement the `CanActAsTool` interface on the sub-agent and define a tool-facing name and description: -->
하위 에이전트가 부모 에이전트에 노출되는 방식을 사용자 지정하려면, 하위 에이전트에서 `CanActAsTool` 인터페이스를 구현하고 툴에 표시될 이름과 설명을 정의합니다:

```php
use Laravel\Ai\Attributes\Provider;
use Laravel\Ai\Contracts\CanActAsTool;
use Laravel\Ai\Enums\Lab;

#[Provider(Lab::Anthropic)]
class RefundsAgent implements Agent, CanActAsTool, HasTools
{
    /**
     * Get the agent's tool name.
     */
    public function name(): string
    {
        return 'refunds_specialist';
    }

    /**
     * Get the agent's tool description.
     */
    public function description(): string
    {
        return 'Determine whether an order is eligible for a refund and explain the next step.';
    }

    // ...
}
```

<!-- If a sub-agent does not implement `CanActAsTool`, Laravel will use the agent's class basename as the tool name and a generic description that asks the parent agent to pass a clear, self-contained task description. Each sub-agent invocation runs in isolation and does not receive the parent agent's conversation history. -->
하위 에이전트가 `CanActAsTool`을 구현하지 않으면 Laravel은 에이전트 클래스의 basename을 툴 이름으로 사용하고, 부모 에이전트가 명확하고 독립적인 작업 설명을 전달하도록 요청하는 기본 설명을 사용합니다. 각 하위 에이전트 호출은 격리되어 실행되며 부모 에이전트의 대화 기록을 받지 않습니다.

<!-- When the parent agent is [streaming](#streaming), its sub-agents stream as well. The parent agent emits `ToolResult` events containing the text the sub-agent has produced so far. These events are marked as preliminary and are followed by the tool call's final result, so you may skip them when iterating events manually: -->
상위 에이전트가 [streaming](#streaming) 중이면 하위 에이전트도 스트리밍합니다. 상위 에이전트는 하위 에이전트가 지금까지 생성한 텍스트가 포함된 `ToolResult` 이벤트를 내보냅니다. 이러한 이벤트는 예비 결과로 표시되며 툴 호출의 최종 결과가 뒤따르므로, 이벤트를 수동으로 반복 처리할 때는 건너뛸 수 있습니다:

```php
use Laravel\Ai\Streaming\Events\ToolResult;

foreach ($stream as $event) {
    if ($event instanceof ToolResult && $event->preliminary) {
        continue;
    }

    // ...
}
```

<!-- Response values such as `text`, `usage`, and `toolResults` ignore preliminary events. The [Vercel protocol](#stream-protocols) renders them as native streaming tool output, so `useChat` displays the progress without any custom code, while the AG-UI protocol reports them as activity snapshots. The completed response's text, reasoning, citations, and usage include those of the sub-agent. -->
`text`, `usage`, `toolResults`와 같은 응답 값은 초기 이벤트를 무시합니다. [Vercel protocol](#stream-protocols)은 이러한 값을 네이티브 스트리밍 툴 출력으로 렌더링하므로 `useChat`은 별도의 커스텀 코드 없이 진행 상황을 표시하며, AG-UI protocol은 이를 활동 스냅샷으로 보고합니다. 완료된 응답의 텍스트, 추론, 인용, 사용량에는 하위 에이전트의 값도 포함됩니다.

<a name="middleware"></a>
<!-- ### Middleware -->
### Middleware

<!-- Agents support middleware, allowing you to intercept and modify each generation step before it is sent to the provider. Middleware is invoked once per step, so a run that takes three steps will invoke it three times. Middleware can be created using the `make:agent-middleware` Artisan command: -->
에이전트는 미들웨어를 지원하므로, 각 생성 단계가 프로바이더로 전송되기 전에 이를 가로채고 수정할 수 있습니다. 미들웨어는 단계마다 한 번씩 호출되므로, 세 단계를 수행하는 실행에서는 미들웨어가 세 번 호출됩니다. `make:agent-middleware` Artisan 명령어를 사용하여 미들웨어를 생성할 수 있습니다.

```shell
php artisan make:agent-middleware LogPrompts
```

<!-- The generated middleware will be placed in your application's `app/Ai/Middleware` directory. To add middleware to an agent, implement the `HasMiddleware` interface and define a `middleware` method that returns an array of middleware classes: -->
생성된 Middleware는 애플리케이션의 `app/Ai/Middleware` 디렉터리에 배치됩니다. 에이전트에 Middleware를 추가하려면 `HasMiddleware` 인터페이스를 구현하고, Middleware 클래스 배열을 반환하는 `middleware` 메서드를 정의합니다.

```php
<?php

namespace App\Ai\Agents;

use App\Ai\Middleware\LogPrompts;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasMiddleware;
use Laravel\Ai\Promptable;

class SalesCoach implements Agent, HasMiddleware
{
    use Promptable;

    // ...

    /**
     * Get the agent's middleware.
     */
    public function middleware(): array
    {
        return [
            new LogPrompts,
        ];
    }
}
```

<!-- Each middleware class should define a `handle` method that receives a `PendingStep` and a `Closure` that passes the step to the next middleware: -->
각 미들웨어 클래스는 `PendingStep`와 해당 스텝을 다음 미들웨어로 전달하는 `Closure`를 받는 `handle` 메서드를 정의해야 합니다:

```php
<?php

namespace App\Ai\Middleware;

use Closure;
use Illuminate\Support\Facades\Log;
use Laravel\Ai\PendingStep;

class LogPrompts
{
    /**
     * Handle the pending generation step.
     */
    public function handle(PendingStep $step, Closure $next)
    {
        Log::info('Prompting agent', ['model' => $step->model]);

        return $next($step);
    }
}
```

<!-- In addition to the `provider`, `model`, `instructions`, `messages`, and `tools` that are about to be sent, the step exposes the steps that have already completed, their combined usage, and the progress of the run: -->
전송될 `provider`, `model`, `instructions`, `messages`, `tools` 외에도 이 단계에서는 이미 완료된 단계, 이들의 통합 사용량, 실행 진행 상황을 확인할 수 있습니다.

```php
$step->steps;
$step->usage;

$step->number;
$step->isFirstStep();
$step->isFinalStep;
```

<!-- The `withModel`, `withInstructions`, `withMessages`, `withTools`, `onlyTools`, `withoutTools`, `withToolChoice`, `withMaxTokens`, and `withProviderOptions` methods each return a copy of the step. For example, you may remove an expensive tool once the agent has used it: -->
`withModel`, `withInstructions`, `withMessages`, `withTools`, `onlyTools`, `withoutTools`, `withToolChoice`, `withMaxTokens`, `withProviderOptions` 메서드는 각각 단계의 복사본을 반환합니다. 예를 들어 에이전트가 비용이 많이 드는 툴을 사용한 후 해당 툴을 제거할 수 있습니다:

```php
public function handle(PendingStep $step, Closure $next)
{
    if (! $step->isFirstStep()) {
        $step = $step->withoutTools('SearchDocumentation');
    }

    return $next($step);
}
```

<!-- Or, you may keep a long tool calling loop within the context window by summarizing the middle of the conversation: -->
또는 대화 중간 부분을 요약해 긴 도구 호출 루프를 컨텍스트 윈도우 안에 유지할 수 있습니다.

```php
use App\Ai\Agents\Summarizer;
use Laravel\Ai\Messages\UserMessage;

public function handle(PendingStep $step, Closure $next)
{
    if (count($step->messages) > 40) {
        $summary = (new Summarizer)->prompt(
            collect(array_slice($step->messages, 1, -10))->map->content->implode("\n"),
        )->text;

        $step = $step->withMessages([
            $step->messages[0],
            new UserMessage("Summary of the conversation so far: {$summary}"),
            ...array_slice($step->messages, -10),
        ]);
    }

    return $next($step);
}
```

<!-- Messages passed to the `withMessages` method only change what is sent for the current step. Later steps and the stored conversation continue to use the full, unsummarized history. -->
`withMessages` 메서드에 전달된 메시지는 현재 단계에서 전송되는 내용만 변경합니다. 이후 단계와 저장된 대화에서는 요약되지 않은 전체 기록을 계속 사용합니다.

<!-- You may use the `then` method to execute code once the model has answered the step, before its tool calls are executed. This works for both synchronous and streaming responses: -->
`then` 메서드를 사용하면 모델이 단계에 답변한 후 툴 호출이 실행되기 전에 코드를 실행할 수 있습니다. 이는 동기 응답과 스트리밍 응답 모두에서 작동합니다:

```php
use Laravel\Ai\Gateway\StepResponse;

public function handle(PendingStep $step, Closure $next)
{
    return $next($step)->then(function (StepResponse $response) {
        Log::info('Agent responded', ['text' => $response->text]);
    });
}
```

<!-- Middleware must return the result of `$next`, or its own `StepResponse` to answer the step without invoking the model, such as when serving a cached response. Returning any other value will throw a `LogicException`. -->
미들웨어는 `$next`의 결과 또는 자체 `StepResponse`를 반환해야 합니다. 캐시된 응답을 제공하는 경우처럼 모델을 호출하지 않고 단계에 응답하려면 자체 StepResponse를 반환할 수 있습니다. 다른 값을 반환하면 `LogicException`이 발생합니다.

<a name="anonymous-agents"></a>
<!-- ### Anonymous Agents -->
### Anonymous Agents

<!-- Sometimes you may want to quickly interact with a model without creating a dedicated agent class. You can create an ad-hoc, anonymous agent using the `agent` function: -->
때로는 전용 에이전트 클래스를 만들지 않고 모델과 빠르게 상호작용하고 싶을 수 있습니다. `agent` 함수를 사용하면 임시 익명 에이전트를 만들 수 있습니다.

```php
use function Laravel\Ai\{agent};

$response = agent(
    instructions: 'You are an expert at software development.',
    messages: [],
    tools: [],
)->prompt('Tell me about Laravel');
```

<!-- Anonymous agents may also produce structured output: -->
익명 에이전트도 구조화된 출력을 생성할 수 있습니다.

```php
use Illuminate\Contracts\JsonSchema\JsonSchema;

use function Laravel\Ai\{agent};

$response = agent(
    schema: fn (JsonSchema $schema) => [
        'number' => $schema->integer()->required(),
    ],
)->prompt('Generate a random number less than 100');
```

<a name="agent-configuration"></a>
<!-- ### Agent Configuration -->
### Agent Configuration

<!-- You may configure text generation options for an agent using PHP attributes. The following attributes are available: -->
PHP 속성을 사용하여 에이전트의 텍스트 생성 옵션을 설정할 수 있습니다. 사용할 수 있는 속성은 다음과 같습니다.

<!-- - `MaxSteps`: The maximum number of steps the agent may take when using tools. - `MaxTokens`: The maximum number of tokens the model may generate. - `Model`: The model the agent should use. - `Provider`: The AI provider (or providers for failover) to use for the agent. - `Temperature`: The sampling temperature to use for generation (0.0 to 1.0). - `Timeout`: The HTTP timeout in seconds for agent requests (default: 60). - `TopP`: The nucleus sampling probability to use for generation (0.0 to 1.0). - `UseCheapestModel`: Use the provider's cheapest text model for cost optimization. - `UseSmartestModel`: Use the provider's most capable text model for complex tasks. -->
- `MaxSteps`: 툴을 사용할 때 에이전트가 수행할 수 있는 최대 단계 수입니다.
- `MaxTokens`: 모델이 생성할 수 있는 최대 토큰 수입니다.
- `Model`: 에이전트가 사용해야 하는 모델입니다.
- `Provider`: 에이전트에 사용할 AI provider입니다. 장애 조치를 위해 여러 provider를 지정할 수도 있습니다.
- `Temperature`: 생성에 사용할 샘플링 temperature입니다(0.0~1.0).
- `Timeout`: 에이전트 요청의 HTTP timeout(초)입니다(기본값: 60).
- `TopP`: 생성에 사용할 nucleus sampling 확률입니다(0.0~1.0).
- `UseCheapestModel`: 비용 최적화를 위해 provider에서 가장 저렴한 텍스트 모델을 사용합니다.
- `UseSmartestModel`: 복잡한 작업을 위해 provider에서 가장 성능이 뛰어난 텍스트 모델을 사용합니다.

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Attributes\MaxSteps;
use Laravel\Ai\Attributes\MaxTokens;
use Laravel\Ai\Attributes\Model;
use Laravel\Ai\Attributes\Provider;
use Laravel\Ai\Attributes\Temperature;
use Laravel\Ai\Attributes\Timeout;
use Laravel\Ai\Attributes\TopP;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Promptable;

#[Provider(Lab::Anthropic)]
#[Model('claude-sonnet-5')]
#[MaxSteps(10)]
#[MaxTokens(4096)]
#[Temperature(0.7)]
#[Timeout(120)]
#[TopP(0.9)]
class SalesCoach implements Agent
{
    use Promptable;

    // ...
}
```

<!-- The `UseCheapestModel` and `UseSmartestModel` attributes allow you to automatically select the most cost-effective or most capable model for a given provider without specifying a model name. This is useful when you want to optimize for cost or capability across different providers: -->
`UseCheapestModel` 및 `UseSmartestModel` 속성을 사용하면 모델 이름을 지정하지 않아도 지정된 provider에서 가장 비용 효율적인 모델이나 가장 성능이 뛰어난 모델을 자동으로 선택할 수 있습니다. 여러 provider에서 비용 또는 성능을 기준으로 최적화하고 싶을 때 유용합니다.

```php
use Laravel\Ai\Attributes\UseCheapestModel;
use Laravel\Ai\Attributes\UseSmartestModel;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Promptable;

#[UseCheapestModel]
class SimpleSummarizer implements Agent
{
    use Promptable;

    // Will use the cheapest model (e.g., Haiku)...
}

#[UseSmartestModel]
class ComplexReasoner implements Agent
{
    use Promptable;

    // Will use the most capable model (e.g., Opus)...
}
```

> [!NOTE]
> `UseCheapestModel` 및 `UseSmartestModel`이 선택하는 기반 모델은 프로바이더가 새로운 모델을 출시함에 따라 Laravel AI SDK 릴리스 간에 변경될 수 있습니다. 모델을 전환하면 동작 변경, 더 이상 사용되지 않는 파라미터, 상당한 비용 차이가 발생할 수 있습니다. 안정적이고 예측 가능한 모델과 가격이 필요하다면 `Model` 속성을 사용해 모델을 명시적으로 지정하세요.

<a name="provider-options"></a>
<!-- ### Provider Options -->
### Provider Options

<!-- If your agent needs to pass provider-specific options (such as OpenAI reasoning effort or penalty settings), implement the `HasProviderOptions` contract and define a `providerOptions` method: -->
에이전트가 OpenAI의 추론 노력 수준이나 패널티 설정처럼 provider별 옵션을 전달해야 한다면, `HasProviderOptions` contract를 구현하고 `providerOptions` 메서드를 정의합니다.

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasProviderOptions;
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Promptable;

class SalesCoach implements Agent, HasProviderOptions
{
    use Promptable;

    // ...

    /**
     * Get provider-specific generation options.
     */
    public function providerOptions(Lab|string $provider): array
    {
        return match ($provider) {
            Lab::OpenAI => [
                'reasoning' => ['effort' => 'low'],
                'frequency_penalty' => 0.5,
                'presence_penalty' => 0.3,
            ],
            Lab::Anthropic => [
                'thinking' => ['budget_tokens' => 1024],
                'cache_control' => ['type' => 'ephemeral'],
            ],
            default => [],
        };
    }
}
```

<!-- The `providerOptions` method receives the provider currently being used (`Lab` enum or string), allowing you to return different options per provider. This is especially useful when using [failover](#failover), since each fallback provider can receive its own configuration. -->
`providerOptions` 메서드는 현재 사용 중인 프로바이더(`Lab` enum 또는 문자열)를 받으므로, 프로바이더별로 서로 다른 옵션을 반환할 수 있습니다. 이는 [failover](#failover)를 사용할 때 특히 유용합니다. 각 fallback 프로바이더가 고유한 설정을 받을 수 있기 때문입니다.

<!-- The Anthropic example above also enables [prompt caching](#prompt-caching) via `cache_control`. -->
위의 Anthropic 예제에서는 `cache_control`을 통해 [prompt caching](#prompt-caching)도 활성화합니다.

<!-- The [image](#images), [audio](#audio), [transcription](#transcription), [embedding](#embeddings), and [reranking](#reranking) builders accept provider options as well: -->
[image](#images), [audio](#audio), [transcription](#transcription), [embedding](#embeddings), [reranking](#reranking) 빌더는 프로바이더 옵션도 허용합니다:

```php
use Laravel\Ai\Audio;

$audio = Audio::of('I love coding with Laravel.')
    ->withProviderOptions(['speed' => 1.25])
    ->generate();
```

<!-- You may also pass a closure instead of an array, which will receive the provider currently being used. -->
배열 대신 클로저를 전달할 수도 있으며, 이 클로저는 현재 사용 중인 프로바이더를 전달받습니다.

<a name="custom-http-headers"></a>
<!-- #### Custom HTTP Headers -->
#### Custom HTTP Headers

<!-- Headers configured for a provider within your application's `config/ai.php` configuration file are sent with every request that provider makes. To send headers on a per-request basis, such as metadata used by an AI gateway, you may use the `withHeaders` method, which is available on the image, audio, transcription, embedding, and reranking builders, as well as on [file uploads](#files): -->
애플리케이션의 `config/ai.php` 설정 파일에서 프로바이더에 구성한 헤더는 해당 프로바이더가 보내는 모든 요청에 함께 전송됩니다. AI 게이트웨이에서 사용하는 메타데이터처럼 요청별로 헤더를 전송하려면 이미지, 오디오, 전사, 임베딩, 리랭킹 빌더와 [file uploads](#files)에서 사용할 수 있는 `withHeaders` 메서드를 사용하면 됩니다.

```php
use Laravel\Ai\Embeddings;

$embeddings = Embeddings::for($chunks)
    ->withHeaders(['cf-aig-metadata' => json_encode(['team' => $team->id])])
    ->withProviderOptions(['dimensions' => 1024])
    ->generate();
```

<!-- Headers may also be given as a closure, which receives the provider currently being used. Headers are not included in the request body and do not affect [embedding cache keys](#caching-embeddings). -->
헤더는 현재 사용 중인 프로바이더를 인수로 받는 클로저로 지정할 수도 있습니다. 헤더는 요청 본문에 포함되지 않으며 [embedding cache keys](#caching-embeddings)에 영향을 주지 않습니다.

<a name="prompt-caching"></a>
<!-- ### Prompt Caching -->
### Prompt Caching

<!-- Most providers cache repeated prompt prefixes automatically and bill the cached portion at a discount. OpenAI, Gemini, Groq, DeepSeek, and xAI require no configuration, and you may inspect the savings via the response's usage: -->
대부분의 프로바이더는 반복되는 프롬프트 접두사를 자동으로 캐시하고, 캐시된 부분에는 할인된 요금을 적용합니다. OpenAI, Gemini, Groq, DeepSeek, xAI는 별도의 설정이 필요하지 않으며, 응답의 usage를 통해 절감된 비용을 확인할 수 있습니다.

```php
$response->usage->cacheReadInputTokens;
$response->usage->cacheWriteInputTokens;
```

<!-- Both of these counts are subsets of the input token total, which is discussed further in the [usage documentation](#usage). -->
이 두 카운트는 모두 입력 토큰 총계의 하위 집합이며, 자세한 내용은 [usage documentation](#usage)에서 설명합니다.

<!-- The `anthropic` and `bedrock` providers only cache when asked. The `CacheInstructions` and `CacheToolDefinitions` attributes place a cache breakpoint at the end of your agent's instructions and tool definitions, so every conversation reads that prefix from the cache instead of writing it again: -->
`anthropic` 및 `bedrock` 프로바이더는 요청한 경우에만 캐시합니다. `CacheInstructions` 및 `CacheToolDefinitions` 속성은 에이전트의 지침과 툴 정의 끝에 캐시 중단점을 배치하므로, 모든 대화는 해당 접두사를 다시 기록하는 대신 캐시에서 읽습니다:

```php
use Laravel\Ai\Attributes\CacheInstructions;
use Laravel\Ai\Attributes\CacheToolDefinitions;

#[CacheInstructions]
#[CacheToolDefinitions]
class SalesCoach implements Agent
{
    use Promptable;

    // ...
}
```

<!-- If your instructions change on every request, such as when they embed the current date, use `CacheToolDefinitions` alone. Caching a prefix that changes on every request creates a new cache entry each time, so you pay to write it to the cache without ever reusing it. -->
지침이 모든 요청마다 변경되는 경우(예: 현재 날짜를 포함하는 경우)에는 `CacheToolDefinitions`만 사용하세요. 모든 요청마다 변경되는 접두사를 캐시하면 매번 새로운 캐시 항목이 생성되므로, 이를 재사용하지도 못한 채 캐시에 기록하는 비용만 지불하게 됩니다.

<!-- Providers that do not support these attributes ignore them, so an agent may safely declare them while using [failover](#failover). -->
이러한 속성을 지원하지 않는 프로바이더는 해당 속성을 무시하므로, 에이전트는 [failover](#failover)를 사용하면서도 이를 안전하게 선언할 수 있습니다.

<!-- Cached prefixes are retained for five minutes by default. Anthropic may retain them for an hour if you pass a TTL to the attribute: -->
캐시된 접두사는 기본적으로 5분 동안 유지됩니다. 속성에 TTL을 전달하면 Anthropic이 최대 1시간 동안 유지할 수 있습니다.

```php
#[CacheInstructions('1h')]
#[CacheToolDefinitions('1h')]
```

<!-- Alternatively, Anthropic's automatic caching may be enabled via a top-level `cache_control` [provider option](#provider-options). This places a single breakpoint after the last block of the request, so the breakpoint advances as the conversation grows and each turn reads the previous turns from the cache. Both mechanisms may be combined. -->
또는 최상위 `cache_control` [provider option](#provider-options)을 통해 Anthropic의 자동 캐싱을 활성화할 수 있습니다. 이렇게 하면 요청의 마지막 블록 다음에 단일 중단점이 설정되므로, 대화가 길어질수록 중단점이 앞으로 이동하고 각 턴은 이전 턴을 캐시에서 읽습니다. 두 메커니즘을 함께 사용할 수도 있습니다.

> [!WARNING]
> 프로바이더는 툴, 지침, 메시지 순서로 프롬프트를 구성하므로, 지침을 한 시간 동안 캐시하려면 툴 정의도 한 시간 동안 캐시해야 합니다. 두 가지를 혼합하면 `InvalidArgumentException`이 발생합니다.

<a name="human-tool-approval"></a>
<!-- ## Human Tool Approval -->
## Human Tool Approval

> [!WARNING]
> 도구 승인을 사용하려면 실행이 재개될 때 일시 중지된 턴의 기록을 사용할 수 있어야 합니다. `RemembersConversations` 트레이트를 사용하는 `Conversational` 에이전트와 같은 에이전트를 사용하거나, 애플리케이션 프런트엔드에서 [`withMessages` method](#conversation-context)를 사용해 기록을 제공해야 합니다. 어느 방법도 사용하지 않는 에이전트는 도구가 일시 중지될 때 `ApprovalNotResumableException`을 발생시킵니다.

<!-- Tools that perform sensitive or irreversible actions may require human approval before they are executed. To make a tool approvable, implement the `Approvable` contract and use the `InteractsWithApprovals` trait. Approvable tools require approval by default: -->
민감하거나 되돌릴 수 없는 작업을 수행하는 툴은 실행 전에 사람의 승인을 요구할 수 있습니다. 툴을 승인 가능하게 만들려면 `Approvable` 컨트랙트를 구현하고 `InteractsWithApprovals` 트레이트를 사용합니다. 승인 가능한 툴은 기본적으로 승인이 필요합니다:

```php
<?php

namespace App\Ai\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Illuminate\Support\Facades\Storage;
use Laravel\Ai\Concerns\InteractsWithApprovals;
use Laravel\Ai\Contracts\Approvable;
use Laravel\Ai\Contracts\Tool;
use Laravel\Ai\Tools\Request;
use Stringable;

class DeleteFile implements Approvable, Tool
{
    use InteractsWithApprovals;

    /**
     * Get the description of the tool's purpose.
     */
    public function description(): Stringable|string
    {
        return 'Delete a file from storage.';
    }

    /**
     * Execute the tool.
     */
    public function handle(Request $request): Stringable|string
    {
        Storage::delete($request['path']);

        return "Deleted [{$request['path']}].";
    }

    /**
     * Get the tool's schema definition.
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'path' => $schema->string()->required(),
        ];
    }
}
```

<!-- To determine whether approval is needed based on the tool call's arguments, define a `needsApproval` method on the tool. This method may return a boolean or an `Approval` instance that includes a reason for the approval request: -->
도구 호출의 인수를 바탕으로 승인이 필요한지 판단하려면 도구에 `needsApproval` 메서드를 정의합니다. 이 메서드는 불리언 값이나 승인 요청 사유를 포함하는 `Approval` 인스턴스를 반환할 수 있습니다.

```php
use Laravel\Ai\Approvals\Approval;

/**
 * Determine whether the tool needs approval for the given request.
 */
protected function needsApproval(Request $request): Approval|bool
{
    return str_starts_with($request['path'], 'temporary/')
        ? false
        : Approval::required('This will permanently delete a file.');
}
```

<!-- You may override a tool's approval requirement when returning it from an agent's `tools` method: -->
에이전트의 `tools` 메서드에서 반환할 때 도구의 승인 요구 사항을 재정의할 수 있습니다:

```php
public function tools(): iterable
{
    return [
        (new SendNotification)->withoutApproval(),
        (new DeleteFile)->requireApproval('Deletion review required.'),
    ];
}
```

<!-- When an approvable tool is called, the agent pauses before executing it. You may inspect the response's pending approvals, which contain each tool call's ID, tool name, arguments, and approval reason: -->
승인 가능한 툴을 호출하면 에이전트는 실행 전에 일시 중지합니다. 응답의 대기 중인 승인을 확인할 수 있으며, 여기에는 각 툴 호출의 ID, 툴 이름, 인수, 승인 사유가 포함됩니다.

```php
$response = (new FileAssistant)
    ->forUser($user)
    ->prompt('Delete the old invoice.');

if ($response->hasPendingApprovals()) {
    foreach ($response->pendingApprovals as $approval) {
        // $approval->id
        // $approval->tool
        // $approval->arguments
        // $approval->reason
    }
}
```

<!-- To resume the agent, continue the conversation and provide a `Decisions` instance containing a decision for each pending tool call. Decisions may approve the call, reject it, or edit its arguments before execution: -->
에이전트를 재개하려면 대화를 계속 진행하고, 보류 중인 각 툴 호출에 대한 결정을 포함하는 `Decisions` 인스턴스를 제공해야 합니다. 결정에 따라 호출을 승인하거나 거부하거나, 실행 전에 인수를 수정할 수 있습니다.

```php
use Laravel\Ai\Approvals\Decision;
use Laravel\Ai\Approvals\Decisions;

$response = (new FileAssistant)
    ->continue($conversationId, as: $user)
    ->prompt(Decisions::from([
        'call_abc' => Decision::approve(),
        'call_ghi' => Decision::reject('The invoice must be retained.'),
    ]));
```

> [!IMPORTANT]
> 일시 중지된 턴은 일시 중지한 참여자가 아니라 대화와 대기 중인 툴 호출을 기준으로 매칭됩니다. 따라서 애플리케이션은 [complete approval flow](#complete-approval-flow)에 설명된 것처럼 대화를 재개하기 전에 대화에 대한 액세스를 인가하거나, 대화 스토어의 `conversationBelongsTo` 메서드를 사용해 액세스 권한을 확인해야 합니다.

<!-- The boolean values `true` and `false` may be used as shorthand for approval and rejection. Every pending tool call must receive a decision. Unknown, missing, or previously resolved tool call IDs will cause an `ApprovalMismatchException` to be thrown. You may provide a default for calls without an explicit decision using the `approveRemaining` or `rejectRemaining` methods: -->
불리언 값인 `true`와 `false`는 승인과 거부를 나타내는 축약형으로 사용할 수 있습니다. 대기 중인 모든 도구 호출에는 결정을 내려야 합니다. 알 수 없거나 누락된 도구 호출 ID 또는 이미 해결된 도구 호출 ID를 전달하면 `ApprovalMismatchException`이 발생합니다. 명시적인 결정을 내리지 않은 호출에는 `approveRemaining` 또는 `rejectRemaining` 메서드를 사용해 기본값을 지정할 수 있습니다:

```php
$decisions = Decisions::from([
    'call_abc' => true,
])->rejectRemaining('Not approved.');

$response = (new FileAssistant)
    ->continue($conversationId, as: $user)
    ->prompt($decisions);
```

<!-- A rejection with a result, such as `Decision::reject('Not approved.')`, is returned to the model so it may continue responding. A rejection without a result stops the generation loop after recording the rejection. -->
`Decision::reject('Not approved.')`와 같은 결과가 포함된 거부는 모델에 반환되므로 모델이 계속 응답할 수 있습니다. 결과가 없는 거부는 거부를 기록한 후 생성 루프를 중지합니다.

<!-- Tool approval is supported by the `prompt`, `stream`, `queue`, `broadcast`, `broadcastNow`, and `broadcastOnQueue` methods. -->
`prompt`, `stream`, `queue`, `broadcast`, `broadcastNow`, `broadcastOnQueue` 메서드는 툴 승인을 지원합니다.

<!-- During streaming and broadcasting, a pause is represented by a `tool_approval_request` event. When using the [Vercel AI SDK stream protocol](#stream-protocols), approval requests and results are emitted using the protocol's native tool approval parts, and the Agent User Interaction protocol reports them as interrupts. -->
스트리밍 및 브로드캐스팅 중 일시 중지는 `tool_approval_request` 이벤트로 나타납니다. [Vercel AI SDK stream protocol](#stream-protocols)을 사용할 때 승인 요청과 결과는 해당 프로토콜의 네이티브 툴 승인 파트를 사용해 방출되며, Agent User Interaction 프로토콜에서는 이를 인터럽트로 보고합니다.

<!-- Clients that use either protocol post their decisions along with the rest of the conversation, so a [chat request](#frontend-integration) may be passed directly to the agent: -->
두 프로토콜 중 하나를 사용하는 클라이언트는 대화의 나머지 내용과 함께 결정을 전송하므로, [chat request](#frontend-integration)를 에이전트에 직접 전달할 수 있습니다:

```php
$chat = Vercel::chat($request);

return (new FileAssistant)
    ->continue($conversationId, as: $request->user())
    ->stream($chat)
    ->usingProtocol($chat->protocol());
```

<!-- When a paused turn is resumed, the resumed steps are merged into that turn, so each turn is stored as a single assistant message. The response's `assistantMessageId` contains the ID of the paused message, and that message's usage includes both the pause and the resume. -->
일시 중지된 턴을 재개하면 재개된 단계가 해당 턴에 병합되므로 각 턴은 하나의 assistant 메시지로 저장됩니다. 응답의 `assistantMessageId`에는 일시 중지된 메시지의 ID가 포함되며, 해당 메시지의 사용량에는 일시 중지와 재개가 모두 포함됩니다.

<!-- For queued agents, the resulting response is passed to the `then` callback, and Laravel also dispatches a `ToolApprovalRequested` event. -->
큐에 대기 중인 에이전트의 경우 결과 응답이 `then` 콜백으로 전달되며, Laravel은 `ToolApprovalRequested` 이벤트도 디스패치합니다.

<!-- Laravel stores the result of an approved tool before asking the model to continue. If generation then fails, the approval has already been resolved. Continue the conversation with a normal text prompt instead of submitting the same approval decisions again. -->
Laravel은 모델에 계속 진행하도록 요청하기 전에 승인된 툴의 결과를 저장합니다. 이후 생성에 실패하더라도 승인은 이미 처리된 상태입니다. 동일한 승인 결정을 다시 제출하지 말고 일반 텍스트 프롬프트로 대화를 계속 진행하세요.

<a name="complete-approval-flow"></a>
<!-- ### Complete Approval Flow -->
### Complete Approval Flow

<!-- The following route demonstrates a complete approval flow, accepting either a new text prompt or approval decisions from the chat screen. This example assumes the application's `User` model uses the `HasConversations` trait: -->
다음 라우트는 새로운 텍스트 프롬프트 또는 채팅 화면에서 전달된 승인 결정을 받아 전체 승인 흐름을 보여줍니다. 이 예제에서는 애플리케이션의 `User` 모델이 `HasConversations` 트레이트를 사용한다고 가정합니다.

```php
use App\Ai\Agents\FileAssistant;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;
use Illuminate\Support\Facades\Route;
use Illuminate\Validation\Rule;
use Laravel\Ai\Approvals\Decision;
use Laravel\Ai\Approvals\Decisions;
use Laravel\Ai\Models\Conversation;

Route::post('/chat/{conversation}', function (Request $request, Conversation $conversation) {
    Gate::authorize('view', $conversation);

    $validated = $request->validate([
        'message' => ['nullable', 'string', 'required_without:decisions', 'prohibits:decisions'],
        'decisions' => ['nullable', 'array', 'required_without:message', 'prohibits:message'],
        'decisions.*.action' => ['required_with:decisions', Rule::in(['approve', 'reject'])],
        'decisions.*.result' => ['nullable', 'string'],
    ]);

    $prompt = isset($validated['decisions'])
        ? Decisions::from(collect($validated['decisions'])->map(
            fn (array $decision) => match ($decision['action']) {
                'approve' => Decision::approve(),
                'reject' => Decision::reject($decision['result'] ?? null),
            }
        )->all())
        : $validated['message'];

    $response = (new FileAssistant)
        ->continue($conversation->id, as: $request->user())
        ->prompt($prompt);

    return [
        'conversation_id' => $response->conversationId,
        'status' => $response->hasPendingApprovals() ? 'awaiting_approval' : 'complete',
        'message' => $response->text,
        'approvals' => $response->pendingApprovals,
    ];
})->middleware('auth');
```

<!-- When the response status is `awaiting_approval`, the chat screen should render the pending approvals and submit the user's choices to the same endpoint using the tool call ID as each decision's key. Otherwise, the screen may submit a plain `message` value: -->
응답 상태가 `awaiting_approval`이면 채팅 화면은 대기 중인 승인을 렌더링하고, 각 결정의 키로 툴 호출 ID를 사용해 사용자의 선택을 동일한 엔드포인트로 제출해야 합니다. 그렇지 않으면 화면에서 일반 `message` 값을 제출할 수 있습니다:

```json
{
    "decisions": {
        "call_abc": {
            "action": "approve"
        },
        "call_def": {
            "action": "reject",
            "result": "The invoice must be retained."
        }
    }
}
```

<a name="images"></a>
<!-- ## Images -->
## Images

<!-- The `Laravel\Ai\Image` class may be used to generate images using the `openai`, `gemini`, or `xai` providers: -->
`Laravel\Ai\Image` 클래스는 `openai`, `gemini`, `xai` provider를 사용하여 이미지를 생성할 때 사용할 수 있습니다.

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')->generate();

$rawContent = (string) $image;
```

<!-- The `square`, `portrait`, and `landscape` methods may be used to control the aspect ratio of the image, while the `quality` method may be used to guide the model on final image quality (`high`, `medium`, `low`). The `timeout` method may be used to specify the HTTP timeout in seconds: -->
이미지의 종횡비를 제어하려면 `square`, `portrait`, `landscape` 메서드를 사용할 수 있으며, 최종 이미지 품질(`high`, `medium`, `low`)을 모델에 안내하려면 `quality` 메서드를 사용할 수 있습니다. HTTP 제한 시간을 초 단위로 지정하려면 `timeout` 메서드를 사용할 수 있습니다.

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')
    ->quality('high')
    ->landscape()
    ->timeout(120)
    ->generate();
```

<!-- You may attach reference images using the `attachments` method: -->
`attachments` 메서드를 사용하여 참고 이미지를 첨부할 수 있습니다.

```php
use Laravel\Ai\Files;
use Laravel\Ai\Image;

$image = Image::of('Update this photo of me to be in the style of an impressionist painting.')
    ->attachments([
        Files\Image::fromStorage('photo.jpg'),
        // Files\Image::fromPath('/home/laravel/photo.jpg'),
        // Files\Image::fromUrl('https://example.com/photo.jpg'),
        // $request->file('photo'),
    ])
    ->landscape()
    ->generate();
```

<!-- Some providers may generate multiple images in a single request. OpenAI, Azure, and xAI accept an `n` [provider option](#provider-options), and the response will contain every image that was returned: -->
일부 프로바이더는 단일 요청에서 여러 이미지를 생성할 수 있습니다. OpenAI, Azure, xAI는 `n` [provider option](#provider-options)을 허용하며, 응답에는 반환된 모든 이미지가 포함됩니다:

```php
$response = Image::of('A donut sitting on the kitchen counter')
    ->withProviderOptions(['n' => 4])
    ->generate();

count($response);           // 4
$response->images;          // A collection of generated images...
$response->firstImage();    // The first generated image...
```

<!-- Generated images may be easily stored on the default disk configured in your application's `config/filesystems.php` configuration file: -->
생성된 이미지는 애플리케이션의 `config/filesystems.php` 설정 파일에 구성된 기본 disk에 쉽게 저장할 수 있습니다.

```php
$image = Image::of('A donut sitting on the kitchen counter');

$path = $image->store();
$path = $image->storeAs('image.jpg');
$path = $image->storePublicly();
$path = $image->storePubliclyAs('image.jpg');
```

<!-- Image generation may also be queued: -->
이미지 생성은 큐에 넣을 수도 있습니다.

```php
use Laravel\Ai\Image;
use Laravel\Ai\Responses\ImageResponse;

Image::of('A donut sitting on the kitchen counter')
    ->portrait()
    ->queue()
    ->then(function (ImageResponse $image) {
        $path = $image->store();

        // ...
    });
```

<a name="audio"></a>
<!-- ## Audio -->
## Audio

<!-- The `Laravel\Ai\Audio` class may be used to generate audio from the given text: -->
`Laravel\Ai\Audio` 클래스는 주어진 텍스트로부터 오디오를 생성하는 데 사용할 수 있습니다.

```php
use Laravel\Ai\Audio;

$audio = Audio::of('I love coding with Laravel.')->generate();

$rawContent = (string) $audio;
```

<!-- You may also generate audio from a string using the `toAudio` method available via Laravel's `Stringable` class: -->
Laravel의 `Stringable` 클래스를 통해 사용할 수 있는 `toAudio` 메서드를 사용하여 문자열에서 오디오를 생성할 수도 있습니다:

```php
use Illuminate\Support\Str;

$audio = Str::of('I love coding with Laravel.')->toAudio();
```

<!-- The `male`, `female`, and `voice` methods may be used to determine the voice of the generated audio: -->
`male`, `female`, `voice` 메서드는 생성되는 오디오의 음성을 결정하는 데 사용할 수 있습니다.

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->generate();

$audio = Audio::of('I love coding with Laravel.')
    ->voice('voice-id-or-name')
    ->generate();
```

<!-- Similarly, the `instructions` method may be used to dynamically coach the model on how the generated audio should sound: -->
마찬가지로, `instructions` 메서드를 사용하면 생성되는 오디오가 어떻게 들려야 하는지 모델에 동적으로 지시할 수 있습니다.

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->instructions('Said like a pirate')
    ->generate();
```

<!-- Generated audio may be easily stored on the default disk configured in your application's `config/filesystems.php` configuration file: -->
생성된 오디오는 애플리케이션의 `config/filesystems.php` 설정 파일에 구성된 기본 disk에 쉽게 저장할 수 있습니다.

```php
$audio = Audio::of('I love coding with Laravel.')->generate();

$path = $audio->store();
$path = $audio->storeAs('audio.mp3');
$path = $audio->storePublicly();
$path = $audio->storePubliclyAs('audio.mp3');
```

<!-- Audio generation may also be queued: -->
오디오 생성은 큐에 넣을 수도 있습니다.

```php
use Laravel\Ai\Audio;
use Laravel\Ai\Responses\AudioResponse;

Audio::of('I love coding with Laravel.')
    ->queue()
    ->then(function (AudioResponse $audio) {
        $path = $audio->store();

        // ...
    });
```

<a name="transcription"></a>
<!-- ## Transcriptions -->
## Transcriptions

<!-- The `Laravel\Ai\Transcription` class may be used to generate a transcript of the given audio: -->
`Laravel\Ai\Transcription` 클래스는 주어진 오디오의 전사본을 생성하는 데 사용할 수 있습니다.

```php
use Laravel\Ai\Transcription;

$transcript = Transcription::fromPath('/home/laravel/audio.mp3')->generate();
$transcript = Transcription::fromStorage('audio.mp3')->generate();
$transcript = Transcription::fromUpload($request->file('audio'))->generate();

return (string) $transcript;
```

<!-- The `diarize` method may be used to indicate you would like the response to include the diarized transcript in addition to the raw text transcript, allowing you to access the segmented transcript by speaker: -->
`diarize` 메서드는 원본 텍스트 전사본에 더해 화자 분리 전사본도 응답에 포함하고 싶다는 뜻을 나타낼 때 사용할 수 있습니다. 이를 통해 화자별로 나뉜 전사본에 접근할 수 있습니다.

```php
$transcript = Transcription::fromStorage('audio.mp3')
    ->diarize()
    ->generate();
```

<!-- Transcription generation may also be queued: -->
전사 생성은 큐에 넣을 수도 있습니다.

```php
use Laravel\Ai\Transcription;
use Laravel\Ai\Responses\TranscriptionResponse;

Transcription::fromStorage('audio.mp3')
    ->queue()
    ->then(function (TranscriptionResponse $transcript) {
        // ...
    });
```

<a name="text-summarization"></a>
<!-- ## Text Summarization -->
## Text Summarization

<!-- You may summarize text using the `summarize` method available via Laravel's `Stringable` class. By default, the summary will contain no more than three sentences and will be generated using the configured provider's cheapest text model: -->
Laravel의 `Stringable` 클래스에서 제공하는 `summarize` 메서드를 사용해 텍스트를 요약할 수 있습니다. 기본적으로 요약문은 최대 세 문장으로 구성되며, 설정된 프로바이더의 가장 저렴한 텍스트 모델을 사용해 생성됩니다.

```php
use Illuminate\Support\Str;

$summary = Str::of($article)->summarize();
```

<!-- You may specify the maximum number of sentences, provider, model, and timeout used to generate the summary. The `Str` class also offers a static version of the method: -->
요약을 생성할 때 사용할 최대 문장 수, 프로바이더, 모델, 타임아웃을 지정할 수 있습니다. `Str` 클래스는 이 메서드의 정적 버전도 제공합니다:

```php
use Laravel\Ai\Enums\Lab;

$summary = Str::of($article)->summarize(
    sentences: 4,
    provider: Lab::Anthropic,
    model: 'claude-sonnet-5',
    timeout: 30,
);

$summary = Str::summarize($article, sentences: 4);
```

<a name="embeddings"></a>
<!-- ## Embeddings -->
## Embeddings

<!-- You may easily generate vector embeddings for any given string using the new `toEmbeddings` method available via Laravel's `Stringable` class: -->
Laravel의 `Stringable` 클래스를 통해 사용할 수 있는 새로운 `toEmbeddings` 메서드를 사용하면, 주어진 문자열에 대한 벡터 임베딩을 쉽게 생성할 수 있습니다.

```php
use Illuminate\Support\Str;

$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

<!-- Alternatively, you may use the `Embeddings` class to generate embeddings for multiple inputs at once: -->
또는 `Embeddings` 클래스를 사용하여 여러 입력에 대한 임베딩을 한 번에 생성할 수 있습니다.

```php
use Laravel\Ai\Embeddings;

$response = Embeddings::for([
    'Napa Valley has great wine.',
    'Laravel is a PHP framework.',
])->generate();

$response->embeddings; // [[0.123, 0.456, ...], [0.789, 0.012, ...]]
```

<!-- You may specify the dimensions and provider for the embeddings: -->
임베딩에 사용할 차원 수와 프로바이더를 지정할 수 있습니다:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->dimensions(1536)
    ->generate(Lab::OpenAI, 'text-embedding-3-small');
```

<a name="multimodal-embeddings"></a>
<!-- ### Multimodal Embeddings -->
### Multimodal Embeddings

<!-- In addition to strings, the `Embeddings::for` method accepts image, audio, document, and video inputs, allowing you to generate embeddings for non-text content. Gemini supports image, audio, document, and video embeddings, while VoyageAI supports image and video embeddings: -->
문자열뿐만 아니라 `Embeddings::for` 메서드는 이미지, 오디오, 문서, 동영상 입력도 허용하므로 텍스트가 아닌 콘텐츠의 임베딩을 생성할 수 있습니다. Gemini는 이미지, 오디오, 문서, 동영상 임베딩을 지원하며, VoyageAI는 이미지와 동영상 임베딩을 지원합니다:

```php
use Laravel\Ai\Embeddings;
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Files\Image;
use Laravel\Ai\Files\Video;

$response = Embeddings::for([
    'A vineyard at sunset.',
    Image::fromStorage('vineyard.jpg'),
    Video::fromPath('/home/laravel/tour.mp4'),
])->generate(Lab::Gemini);
```

<!-- Multimodal inputs use the same [file classes used for attachments](#attachments). These files may be created from a local path, a filesystem disk, a remote URL, or Base64-encoded content. Images, documents, and videos may also be created from uploaded files, while documents may be created from raw string content: -->
멀티모달 입력은 [file classes used for attachments](#attachments)에 사용되는 것과 동일한 파일 클래스를 사용합니다. 이러한 파일은 로컬 경로, 파일시스템 디스크, 원격 URL 또는 Base64로 인코딩된 콘텐츠에서 생성할 수 있습니다. 이미지, 문서, 동영상은 업로드된 파일에서도 생성할 수 있으며, 문서는 원시 문자열 콘텐츠에서도 생성할 수 있습니다:

```php
use Laravel\Ai\Files\Audio;
use Laravel\Ai\Files\Document;
use Laravel\Ai\Files\Image;
use Laravel\Ai\Files\Video;

Image::fromPath('/home/laravel/photo.jpg');
Image::fromStorage('photo.jpg');
Image::fromUpload($request->file('photo'));

Audio::fromPath('/home/laravel/clip.mp3');
Audio::fromStorage('clip.mp3');
Audio::fromUpload($request->file('clip.mp3'));

Video::fromPath('/home/laravel/video.mp4');
Video::fromStorage('video.mp4');
Video::fromUpload($request->file('video'));

Document::fromUrl('https://example.com/report.pdf');
Document::fromString('Laravel is a PHP framework.', 'text/plain');
Document::fromUpload($request->file('report'));
```

> [!NOTE]
> VoyageAI는 단일 요청에서 원격 URL 미디어와 Base64로 인코딩된 미디어를 함께 사용할 수 없습니다. 로컬 파일, 저장된 파일, 업로드된 파일은 Base64로 인코딩된 콘텐츠로 전송되며, 텍스트 입력은 어느 미디어 소스와도 함께 사용할 수 있습니다. 어떤 멀티모달 모델과 입력을 사용할 수 있는지는 해당 프로바이더의 문서를 참조하세요.

<a name="querying-embeddings"></a>
<!-- ### Querying Embeddings -->
### Querying Embeddings

<!-- Once you have generated embeddings, you will typically store them in a `vector` column in your database for later querying. Laravel provides native support for vector columns on PostgreSQL via the `pgvector` extension and MariaDB. To get started, define a `vector` column in your migration, specifying the number of dimensions: -->
임베딩을 생성한 뒤에는 보통 나중에 쿼리할 수 있도록 데이터베이스의 `vector` 컬럼에 저장합니다. Laravel은 `pgvector` 확장을 사용하는 PostgreSQL과 MariaDB의 벡터 컬럼을 네이티브로 지원합니다. 시작하려면 마이그레이션에서 차원 수를 지정하여 `vector` 컬럼을 정의합니다:

```php
Schema::ensureVectorExtensionExists();

Schema::create('documents', function (Blueprint $table) {
    $table->id();
    $table->string('title');
    $table->text('content');
    $table->vector('embedding', dimensions: 1536);
    $table->timestamps();
});
```

<!-- You may also add a vector index to speed up similarity searches. When calling `index` on a vector column, Laravel will automatically create an HNSW index with cosine distance: -->
유사도 검색 속도를 높이기 위해 벡터 인덱스를 추가할 수도 있습니다. 벡터 컬럼에서 `index`를 호출하면 Laravel이 코사인 거리를 사용하는 HNSW 인덱스를 자동으로 생성합니다:

```php
$table->vector('embedding', dimensions: 1536)->index();
```

<!-- On your Eloquent model, you should cast the vector column using the `AsVector` cast: -->
Eloquent 모델에서는 `AsVector` 캐스트를 사용해 벡터 컬럼을 캐스팅해야 합니다:

```php
use Illuminate\Database\Eloquent\Casts\AsVector;

protected function casts(): array
{
    return [
        'embedding' => AsVector::class,
    ];
}
```

<!-- To query for similar records, use the `whereVectorSimilarTo` method. This method filters results by a minimum cosine similarity (between `0.0` and `1.0`, where `1.0` is identical) and orders the results by similarity: -->
유사한 레코드를 쿼리하려면 `whereVectorSimilarTo` 메서드를 사용합니다. 이 메서드는 최소 코사인 유사도(`0.0`에서 `1.0` 사이이며, `1.0`은 동일함을 의미합니다)를 기준으로 결과를 필터링하고, 유사도 순서로 결과를 정렬합니다:

```php
use App\Models\Document;

$documents = Document::query()
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

<!-- The `$queryEmbedding` may be an array of floats or a plain string. When a string is given, Laravel will automatically generate embeddings for it: -->
`$queryEmbedding`은 부동소수점 숫자 배열이거나 일반 문자열일 수 있습니다. 문자열이 주어지면 Laravel이 해당 문자열의 임베딩을 자동으로 생성합니다:

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', 'best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

<!-- If you need more control, you may use the lower-level `whereVectorDistanceLessThan`, `selectVectorDistance`, and `orderByVectorDistance` methods independently: -->
더 세밀하게 제어해야 한다면 하위 수준의 `whereVectorDistanceLessThan`, `selectVectorDistance`, `orderByVectorDistance` 메서드를 각각 사용할 수 있습니다:

```php
$documents = Document::query()
    ->select('*')
    ->selectVectorDistance('embedding', $queryEmbedding, as: 'distance')
    ->whereVectorDistanceLessThan('embedding', $queryEmbedding, maxDistance: 0.3)
    ->orderByVectorDistance('embedding', $queryEmbedding)
    ->limit(10)
    ->get();
```

<!-- If you would like to give an agent the ability to perform similarity searches as a tool, check out the [Similarity Search](#similarity-search) tool documentation. -->
에이전트가 도구로 유사도 검색을 수행할 수 있게 하려면 [Similarity Search](#similarity-search) 도구 문서를 확인하십시오.

> [!NOTE]
> 현재 벡터 쿼리는 `pgvector` 확장을 사용하는 PostgreSQL 연결과 MariaDB 11.7 이상에서 지원됩니다.

<a name="caching-embeddings"></a>
<!-- ### Caching Embeddings -->
### Caching Embeddings

<!-- Embedding generation can be cached to avoid redundant API calls for identical inputs. To enable caching, set the `ai.caching.embeddings.cache` configuration option to `true`: -->
동일한 입력에 대해 중복 API 호출을 피하기 위해 임베딩 생성을 캐싱할 수 있습니다. 캐싱을 활성화하려면 `ai.caching.embeddings.cache` 설정 옵션을 `true`로 설정합니다:

```php
'caching' => [
    'embeddings' => [
        'cache' => true,
        'store' => env('CACHE_STORE', 'database'),
        'individually' => true,
        // ...
    ],
],
```

<!-- When caching is enabled, embeddings are cached for 30 days. The cache key is based on the provider, model, dimensions, and input content, ensuring that identical requests return cached results while different configurations generate fresh embeddings. -->
캐싱이 활성화되면 임베딩은 30일 동안 캐시됩니다. 캐시 키는 프로바이더, 모델, 차원 수, 입력 내용을 기반으로 생성되므로, 동일한 요청은 캐시된 결과를 반환하고 설정이 다른 요청은 새 임베딩을 생성합니다.

<!-- By default, each input's embedding is cached under its own key, so a later request may hit the cache for inputs it has seen before even when the set of inputs or their order has changed. To instead cache the entire set of inputs under a single key, set the `ai.caching.embeddings.individually` configuration option to `false`. -->
기본적으로 각 입력의 임베딩은 자체 키로 캐시되므로, 입력 집합이나 순서가 변경되더라도 이후 요청에서 이전에 본 입력에 대한 캐시가 사용될 수 있습니다. 전체 입력 집합을 하나의 키로 캐시하려면 `ai.caching.embeddings.individually` 설정 옵션을 `false`로 지정합니다.

<!-- You may also enable caching for a specific request using the `cache` method, even when global caching is disabled: -->
전역 캐싱이 비활성화되어 있어도 `cache` 메서드를 사용하여 특정 요청에 대해 캐싱을 활성화할 수도 있습니다:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache()
    ->generate();
```

<!-- You may specify a custom cache duration in seconds: -->
초 단위로 사용자 지정 캐시 기간을 지정할 수 있습니다:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache(seconds: 3600) // Cache for 1 hour
    ->generate();
```

<!-- The `toEmbeddings` Stringable method also accepts a `cache` argument: -->
`toEmbeddings` Stringable 메서드도 `cache` 인수를 받습니다:

```php
// Cache with default duration...
$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: true);

// Cache for a specific duration...
$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: 3600);
```

<a name="reranking"></a>
<!-- ## Reranking -->
## Reranking

<!-- Reranking allows you to reorder a list of documents based on their relevance to a given query. This is useful for improving search results by using semantic understanding: -->
재순위화는 주어진 쿼리와의 관련성을 기준으로 문서 목록의 순서를 다시 정렬할 수 있게 해줍니다. 이는 의미적 이해를 활용해 검색 결과를 개선하는 데 유용합니다:

<!-- The `Laravel\Ai\Reranking` class may be used to rerank documents: -->
`Laravel\Ai\Reranking` 클래스를 사용하여 문서를 재순위화할 수 있습니다:

```php
use Laravel\Ai\Reranking;

$response = Reranking::of([
    'Django is a Python web framework.',
    'Laravel is a PHP web application framework.',
    'React is a JavaScript library for building user interfaces.',
])->rerank('PHP frameworks');

// Access the top result...
$response->first()->document; // "Laravel is a PHP web application framework."
$response->first()->score;    // 0.95
$response->first()->index;    // 1 (original position)
```

<!-- The `limit` method may be used to restrict the number of results returned, while the `timeout` method may be used to specify the HTTP timeout in seconds, which defaults to 30: -->
`limit` 메서드는 반환되는 결과 수를 제한하는 데 사용할 수 있으며, `timeout` 메서드는 초 단위의 HTTP 타임아웃을 지정하는 데 사용할 수 있습니다. 기본값은 30입니다:

```php
$response = Reranking::of($documents)
    ->limit(5)
    ->timeout(60)
    ->rerank('search query');
```

<a name="reranking-collections"></a>
<!-- ### Reranking Collections -->
### Reranking Collections

<!-- For convenience, Laravel collections may be reranked using the `rerank` macro. The first argument specifies which field(s) to use for reranking, and the second argument is the query: -->
편의를 위해 Laravel 컬렉션은 `rerank` 매크로를 사용하여 재순위화할 수 있습니다. 첫 번째 인수는 재순위화에 사용할 필드를 지정하고, 두 번째 인수는 쿼리입니다:

```php
// Rerank by a single field...
$posts = Post::all()
    ->rerank('body', 'Laravel tutorials');

// Rerank by multiple fields (sent as JSON)...
$reranked = $posts->rerank(['title', 'body'], 'Laravel tutorials');

// Rerank using a closure to build the document...
$reranked = $posts->rerank(
    fn ($post) => $post->title.': '.$post->body,
    'Laravel tutorials'
);
```

<!-- You may also limit the number of results and specify a provider: -->
결과 수를 제한하고 프로바이더를 지정할 수도 있습니다:

```php
$reranked = $posts->rerank(
    by: 'content',
    query: 'Laravel tutorials',
    limit: 10,
    provider: Lab::Cohere,
    timeout: 60,
);
```

<a name="classification"></a>
<!-- ## Classification -->
## Classification

> [!WARNING]
> 분류 기능은 현재 실험 단계이며, AI SDK의 향후 마이너 릴리스에서 API가 변경될 수 있습니다.

<!-- Classification allows you to ask a fixed set of questions about a given string or array of data and receive a typed answer, backed by a probability, for each question instead of free-form text. This is useful for routing, moderation, and scoring, where you need to compare an answer against a threshold or make assertions about it in your tests. -->
분류를 사용하면 주어진 문자열이나 데이터 배열에 대해 정해진 질문 집합을 하고, 자유 형식의 텍스트 대신 각 질문에 대해 확률이 함께 제공되는 타입이 지정된 답변을 받을 수 있습니다. 이는 답변을 임계값과 비교하거나 테스트에서 답변에 대한 단정을 작성해야 하는 라우팅, 모더레이션, 스코어링에 유용합니다.

<!-- The `Laravel\Ai\Classification` class may be used to classify content. Each question is given a key, and the corresponding answer may be retrieved from the response using that key: -->
`Laravel\Ai\Classification` 클래스는 콘텐츠를 분류하는 데 사용할 수 있습니다. 각 질문에는 키가 지정되며, 해당 답변은 그 키를 사용해 응답에서 가져올 수 있습니다.

```php
use Laravel\Ai\Classification;
use Laravel\Ai\Classification\Boolean;
use Laravel\Ai\Classification\Choice;
use Laravel\Ai\Classification\Score;

$result = Classification::of($supportRequest)
    ->questions([
        'urgent' => new Boolean('Does this request need an immediate response?', [
            'true' => 'Explicitly time-sensitive',
            'false' => 'No urgency expressed',
        ]),
        'department' => new Choice('Which team should handle this request?', [
            'billing' => 'Payments, invoices, and refunds',
            'technical' => 'Bugs, outages, and integrations',
            'sales' => 'Pricing, plans, and upgrades',
        ]),
        'frustration' => new Score('How frustrated is the customer?', [
            'Calm',
            'Frustrated',
            'Very angry',
        ]),
    ])
    ->classify();
```

<!-- `Boolean` questions return the probability that the answer is "true". The `isTrue` method may be used to determine whether that probability meets a given threshold, which defaults to `0.5`: -->
`Boolean` 질문은 답변이 "true"일 확률을 반환합니다. `isTrue` 메서드를 사용하면 해당 확률이 지정된 임계값을 충족하는지 확인할 수 있으며, 기본값은 `0.5`입니다.

```php
$result['urgent']->probability;             // 0.94
$result['urgent']->isTrue(threshold: 0.8);  // true
```

<!-- `Choice` questions return one of the given options along with the probability of each option. The `confidence` property indicates how certain the provider is across the full set of probabilities, and will be `null` when the provider is unable to measure it: -->
`Choice` 질문은 주어진 옵션 중 하나와 각 옵션의 확률을 함께 반환합니다. `confidence` 프로퍼티는 전체 확률 집합에 대한 프로바이더의 확신 정도를 나타내며, 프로바이더가 이를 측정할 수 없으면 `null`이 됩니다:

```php
$result['department']->choice;                      // 'technical'
$result['department']->probabilityOf('technical');  // 0.87
$result['department']->probabilities;               // ['billing' => 0.08, 'technical' => 0.87, 'sales' => 0.05]
$result['department']->confidence;                  // 0.82
```

<!-- `Score` questions return a position on the ordered levels that were provided. The `score` property is probability-weighted and may fall between two levels, while the `level` and `label` methods describe the most probable level: -->
`Score` 질문은 제공된 순서가 있는 레벨에서 위치를 반환합니다. `score` 프로퍼티는 확률에 따라 가중치가 적용되므로 두 레벨 사이의 값이 될 수 있지만, `level` 및 `label` 메서드는 가장 확률이 높은 레벨을 설명합니다:

```php
$result['frustration']->score;          // 1.24, the probability-weighted level
$result['frustration']->level();        // 1, the most probable level
$result['frustration']->label();        // 'Frustrated'
$result['frustration']->normalized();   // 0.62, the score as a fraction of the highest level
$result['frustration']->probabilities;  // [0.12, 0.52, 0.36]
```

<!-- The criteria given to a `Boolean` question, the option descriptions given to a `Choice` question, and the levels given to a `Score` question may each be an array when a single sentence is not sufficient. `Choice` questions require at least two options, while `Score` questions require at least two levels. -->
`Boolean` 질문에 제공하는 기준, `Choice` 질문에 제공하는 옵션 설명, `Score` 질문에 제공하는 수준은 각각 한 문장으로 충분하지 않을 때 배열일 수 있습니다. `Choice` 질문에는 최소 두 개의 옵션이 필요하며, `Score` 질문에는 최소 두 개의 수준이 필요합니다.

<!-- The response may be iterated, counted, and accessed as an array. In addition, the `answer` method may be used to retrieve a single answer, while the `collect` method returns all of the answers as a [collection](/docs/13.x/collections): -->
응답은 순회하고 개수를 세거나 배열로 접근할 수 있습니다. 또한 `answer` 메서드를 사용해 단일 답변을 가져올 수 있으며, `collect` 메서드는 모든 답변을 [collection](/docs/13.x/collections)으로 반환합니다.

```php
$result->answer('urgent');
$result->collect();

$result->usage;
$result->meta->provider;
```

<!-- For a single yes or no decision, you may use the `decide` method available via Laravel's `Stringable` class, which returns a boolean instead of a full response. You may describe what a "yes" and a "no" mean, and specify the probability the answer must reach, which defaults to `0.5`: -->
단일 예/아니요 결정을 내려야 한다면 `Stringable` 클래스에서 사용할 수 있는 `decide` 메서드를 사용할 수 있습니다. 이 메서드는 전체 응답 대신 불리언을 반환합니다. "예"와 "아니요"가 의미하는 내용을 설명하고, 답변이 도달해야 하는 확률을 지정할 수도 있으며, 기본값은 `0.5`입니다:

```php
use Illuminate\Support\Str;

if (Str::of($message)->decide('Is this spam?')) {
    // ...
}

$spam = Str::of($message)->decide('Is this spam?', criteria: [
    'true' => 'Unsolicited bulk mail.',
    'false' => 'A genuine message from a customer.',
], threshold: 0.9);
```

<!-- By default, classification is performed by [TypeSafe](https://typesafe.ai). You may change this using the `default_for_classification` option within your application's `config/ai.php` configuration file. You may also specify the provider and model when classifying: -->
기본적으로 분류는 [TypeSafe](https://typesafe.ai)가 수행합니다. 애플리케이션의 `config/ai.php` 설정 파일에서 `default_for_classification` 옵션을 사용해 이를 변경할 수 있습니다. 분류할 때 프로바이더와 모델을 지정할 수도 있습니다.

```php
use Laravel\Ai\Enums\Lab;

$result = Classification::of($supportRequest)
    ->questions($questions)
    ->classify(Lab::OpenRouter, 'model-name');
```

<!-- The `timeout` method may be used to specify the HTTP timeout in seconds, which defaults to 30. [Provider options](#provider-options) and custom headers may be given as well: -->
`timeout` 메서드를 사용하면 HTTP 타임아웃을 초 단위로 지정할 수 있으며, 기본값은 30초입니다. [Provider options](#provider-options)과 사용자 지정 헤더도 지정할 수 있습니다.

```php
$result = Classification::of($supportRequest)
    ->questions($questions)
    ->timeout(60)
    ->withProviderOptions(['temperature' => 0])
    ->classify();
```

<a name="files"></a>
<!-- ## Files -->
## Files

<!-- The `Laravel\Ai\Files` class or the individual file classes may be used to store files with your AI provider for later use in conversations. This is useful for large documents or files you want to reference multiple times without re-uploading: -->
`Laravel\Ai\Files` 클래스 또는 개별 파일 클래스를 사용하여 나중에 대화에서 사용할 파일을 AI 프로바이더에 저장할 수 있습니다. 다시 업로드하지 않고 여러 번 참조하려는 큰 문서나 파일에 유용합니다:

```php
use Laravel\Ai\Files\Document;
use Laravel\Ai\Files\Image;

// Store a file from a local path...
$response = Document::fromPath('/home/laravel/document.pdf')->put();
$response = Image::fromPath('/home/laravel/photo.jpg')->put();

// Store a file that is stored on a filesystem disk...
$response = Document::fromStorage('document.pdf', disk: 'local')->put();
$response = Image::fromStorage('photo.jpg', disk: 'local')->put();

// Store a file that is stored on a remote URL...
$response = Document::fromUrl('https://example.com/document.pdf')->put();
$response = Image::fromUrl('https://example.com/photo.jpg')->put();

return $response->id;
```

<!-- You may also store raw content or uploaded files: -->
원시 콘텐츠나 업로드된 파일도 저장할 수 있습니다:

```php
use Laravel\Ai\Files;
use Laravel\Ai\Files\Document;

// Store raw content...
$stored = Document::fromString('Hello, World!', 'text/plain')->put();

// Store an uploaded file...
$stored = Document::fromUpload($request->file('document'))->put();
```

<!-- Once a file has been stored, you may reference the file when generating text via agents instead of re-uploading the file: -->
파일이 저장되면, 해당 파일을 다시 업로드하는 대신 에이전트를 통해 텍스트를 생성할 때 파일을 참조할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Files;

$response = (new SalesCoach)->prompt(
    'Analyze the attached sales transcript...',
    attachments: [
        Files\Document::fromId('file-id') // Attach a stored document...
    ]
);
```

<!-- To retrieve a previously stored file, use the `get` method on a file instance: -->
이전에 저장한 파일을 가져오려면 파일 인스턴스에서 `get` 메서드를 사용합니다:

```php
use Laravel\Ai\Files\Document;

$file = Document::fromId('file-id')->get();

$file->id;
$file->mimeType();
```

<!-- To delete a file from the provider, use the `delete` method: -->
프로바이더에서 파일을 삭제하려면 `delete` 메서드를 사용합니다:

```php
Document::fromId('file-id')->delete();
```

<!-- By default, the `Files` class uses the default AI provider configured in your application's `config/ai.php` configuration file. For most operations, you may specify a different provider using the `provider` argument: -->
기본적으로 `Files` 클래스는 애플리케이션의 `config/ai.php` 설정 파일에 구성된 기본 AI 프로바이더를 사용합니다. 대부분의 작업에서는 `provider` 인수를 사용하여 다른 프로바이더를 지정할 수 있습니다:

```php
$response = Document::fromPath(
    '/home/laravel/document.pdf'
)->put(provider: Lab::Anthropic);
```

<!-- You may pass provider-specific upload options using the `withProviderOptions` method. For example, you may set OpenAI's file `purpose`: -->
`withProviderOptions` 메서드를 사용해 제공자별 업로드 옵션을 전달할 수 있습니다. 예를 들어 OpenAI 파일의 `purpose`를 설정할 수 있습니다:

```php
use Laravel\Ai\Files\Document;

$response = Document::fromPath('/home/laravel/knowledge.txt')
    ->withProviderOptions(['purpose' => 'assistants'])
    ->put();
```

<!-- To scope options per provider, pass a closure that receives the current provider: -->
제공자별로 옵션 범위를 지정하려면 현재 제공자를 받는 클로저를 전달합니다:

```php
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Files\Document;

$response = Document::fromPath('/home/laravel/training.jsonl')
    ->withProviderOptions(fn (Lab|string $provider) => match ($provider) {
        Lab::OpenAI => ['purpose' => 'fine-tune'],
        default => [],
    })
    ->put();
```

<a name="using-stored-files-in-conversations"></a>
<!-- ### Using Stored Files in Conversations -->
### Using Stored Files in Conversations

<!-- Once a file has been stored with a provider, you may reference it in agent conversations using the `fromId` method on the `Document` or `Image` classes: -->
파일이 프로바이더에 저장되면 `Document` 또는 `Image` 클래스의 `fromId` 메서드를 사용하여 에이전트 대화에서 해당 파일을 참조할 수 있습니다:

```php
use App\Ai\Agents\DocumentAnalyzer;
use Laravel\Ai\Files;
use Laravel\Ai\Files\Document;

$stored = Document::fromPath('/path/to/report.pdf')->put();

$response = (new DocumentAnalyzer)->prompt(
    'Summarize this document.',
    attachments: [
        Document::fromId($stored->id),
    ],
);
```

<!-- Similarly, stored images may be referenced using the `Image` class: -->
마찬가지로 저장된 이미지는 `Image` 클래스를 사용하여 참조할 수 있습니다:

```php
use Laravel\Ai\Files;
use Laravel\Ai\Files\Image;

$stored = Image::fromPath('/path/to/photo.jpg')->put();

$response = (new ImageAnalyzer)->prompt(
    'What is in this image?',
    attachments: [
        Image::fromId($stored->id),
    ],
);
```

<a name="vector-stores"></a>
<!-- ## Vector Stores -->
## Vector Stores

<!-- Vector stores allow you to create searchable collections of files that can be used for retrieval-augmented generation (RAG). The `Laravel\Ai\Stores` class provides methods for creating, retrieving, and deleting vector stores: -->
벡터 스토어를 사용하면 검색 증강 생성(RAG)에 사용할 수 있는 검색 가능한 파일 컬렉션을 만들 수 있습니다. `Laravel\Ai\Stores` 클래스는 벡터 스토어를 생성하고, 가져오고, 삭제하는 메서드를 제공합니다:

```php
use Laravel\Ai\Stores;

// Create a new vector store...
$store = Stores::create('Knowledge Base');

// Create a store with additional options...
$store = Stores::create(
    name: 'Knowledge Base',
    description: 'Documentation and reference materials.',
    expiresWhenIdleFor: days(30),
);

return $store->id;
```

<!-- To retrieve an existing vector store by its ID, use the `get` method: -->
기존 벡터 스토어를 ID로 가져오려면 `get` 메서드를 사용합니다:

```php
use Laravel\Ai\Stores;

$store = Stores::get('store_id');

$store->id;
$store->name;
$store->fileCounts;
$store->ready;
```

<!-- To delete a vector store, use the `delete` method on the `Stores` class or the store instance: -->
벡터 스토어를 삭제하려면 `Stores` 클래스 또는 스토어 인스턴스에서 `delete` 메서드를 사용합니다:

```php
use Laravel\Ai\Stores;

// Delete by ID...
Stores::delete('store_id');

// Or delete via a store instance...
$store = Stores::get('store_id');

$store->delete();
```

<a name="adding-files-to-stores"></a>
<!-- ### Adding Files to Stores -->
### Adding Files to Stores

<!-- Once you have a vector store, you may add [files](#files) to it using the `add` method. Files added to a store are automatically indexed for semantic searching using the [file search provider tool](#file-search): -->
벡터 스토어가 준비되면 `add` 메서드를 사용하여 [files](#files)을 추가할 수 있습니다. 스토어에 추가된 파일은 [file search provider tool](#file-search)를 사용한 의미 검색을 위해 자동으로 인덱싱됩니다:

```php
use Laravel\Ai\Files\Document;
use Laravel\Ai\Stores;

$store = Stores::get('store_id');

// Add a file that has already been stored with the provider...
$document = $store->add('file_id');
$document = $store->add(Document::fromId('file_id'));

// Or, store and add a file in one step...
$document = $store->add(Document::fromPath('/path/to/document.pdf'));
$document = $store->add(Document::fromStorage('manual.pdf'));
$document = $store->add($request->file('document'));

$document->id;
$document->fileId;
```

> [!NOTE]
> 일반적으로 이전에 저장한 파일을 벡터 스토어에 추가하면 반환되는 문서 ID가 파일에 이전에 할당된 ID와 일치합니다. 하지만 일부 벡터 스토리지 프로바이더는 새롭고 다른 "문서 ID"를 반환할 수 있습니다. 따라서 나중에 참조할 수 있도록 데이터베이스에 두 ID를 항상 모두 저장하는 것이 좋습니다.

<!-- When adding a file to a Gemini store, Laravel waits for the import to finish so that the document is searchable once the call returns. A `Laravel\Ai\Exceptions\AiException` will be thrown if the import fails or exceeds five minutes, so you may wish to add Gemini files from a [queued job](/docs/13.x/queues). -->
Gemini 스토어에 파일을 추가하면 Laravel은 호출이 반환된 후 문서를 검색할 수 있도록 가져오기가 완료될 때까지 기다립니다. 가져오기에 실패하거나 5분을 초과하면 `Laravel\Ai\Exceptions\AiException`이 발생하므로, [queued job](/docs/13.x/queues)에서 Gemini 파일을 추가하는 것이 좋습니다.

<!-- You may attach metadata to files when adding them to a store. This metadata can later be used to filter search results when using the [file search provider tool](#file-search): -->
파일을 저장소에 추가할 때 메타데이터를 첨부할 수 있습니다. 이 메타데이터는 나중에 [file search provider tool](#file-search)를 사용할 때 검색 결과를 필터링하는 데 사용할 수 있습니다:

```php
$store->add(Document::fromPath('/path/to/document.pdf'), metadata: [
    'author' => 'Taylor Otwell',
    'department' => 'Engineering',
    'year' => 2026,
]);
```

<!-- To remove a file from a store, use the `remove` method: -->
저장소에서 파일을 제거하려면 `remove` 메서드를 사용합니다:

```php
$store->remove('file_id');
```

<!-- Removing a file from a vector store does not remove it from the provider's [file storage](#files). To remove a file from the vector store and delete it permanently from file storage, use the `deleteFile` argument: -->
벡터 스토어에서 파일을 제거해도 프로바이더의 [file storage](#files)에서는 제거되지 않습니다. 벡터 스토어에서 파일을 제거하고 파일 저장소에서도 영구적으로 삭제하려면 `deleteFile` 인수를 사용합니다:

```php
$store->remove('file_abc123', deleteFile: true);
```

<a name="usage"></a>
<!-- ## Usage -->
## Usage

<!-- Every response contains a `usage` property containing the token counts reported by the provider. The input and output counts are totals, so tokens counted as cached or reasoning tokens are also included in the total they belong to: -->
모든 응답에는 프로바이더가 보고한 토큰 수를 포함하는 `usage` 속성이 있습니다. 입력 및 출력 수는 총합이므로, 캐시된 토큰이나 추론 토큰으로 계산된 토큰도 해당 총합에 포함됩니다:

```php
$response = (new SalesCoach)->prompt('Analyze this sales transcript...');

$response->usage->inputTokens;
$response->usage->outputTokens;
$response->usage->totalTokens();
```

<!-- Text generation returns a `Laravel\Ai\Responses\Data\TextUsage` instance, which breaks these totals down further. Each of these values will be `null`, rather than `0`, when the provider does not report it: -->
텍스트 생성은 이러한 총계를 더 자세히 구분해 제공하는 `Laravel\Ai\Responses\Data\TextUsage` 인스턴스를 반환합니다. 프로바이더가 값을 보고하지 않으면 각 값은 `0`이 아니라 `null`이 됩니다.

```php
$response->usage->cacheReadInputTokens; // Subset of the input tokens read from a prompt cache...
$response->usage->cacheWriteInputTokens; // Subset of the input tokens written to a prompt cache...
$response->usage->reasoningTokens; // Subset of the output tokens spent on reasoning...

$response->usage->uncachedInputTokens(); // Input tokens that were neither read from nor written to the cache...
```

<!-- Cache reads, cache writes, and uncached input are billed at different rates, so you should price these three counts separately instead of using the input total alone. -->
캐시 읽기, 캐시 쓰기, 캐시되지 않은 입력에는 서로 다른 요금이 부과되므로 입력 총량만 사용하는 대신 이 세 가지 수치를 별도로 산정해야 합니다.

<!-- The remaining capabilities return a usage object containing the counts specific to them: -->
나머지 기능은 해당 기능에 특화된 카운트를 포함하는 사용량 객체를 반환합니다:

<div class="overflow-auto">

<!-- | Capability | Usage object | Adds | |---|---|---| | Text, classification | `TextUsage` | Cache read, cache write, and reasoning tokens | | Images | `ImageUsage` | `imageInputTokens` and `imageOutputTokens` | | Transcription | `TranscriptionUsage` | `audioSeconds`, the duration of the transcribed audio | | Reranking | `RerankingUsage` | `searchUnits`, which some providers bill instead of tokens | | Audio, embeddings | `Usage` | | -->
| 기능 | 사용량 객체 | 추가 항목 |
|---|---|---|
| 텍스트, 분류 | `TextUsage` | 캐시 읽기, 캐시 쓰기 및 추론 토큰 |
| 이미지 | `ImageUsage` | `imageInputTokens` 및 `imageOutputTokens` |
| 전사 | `TranscriptionUsage` | `audioSeconds`, 전사된 오디오의 길이 |
| 리랭킹 | `RerankingUsage` | `searchUnits`, 일부 프로바이더가 토큰 대신 과금하는 단위 |
| 오디오, 임베딩 | `Usage` | |

</div>

<!-- Not every provider reports every count, and counts that a provider does not report will be `null`: -->
모든 프로바이더가 모든 개수를 보고하는 것은 아니며, 프로바이더가 보고하지 않는 개수는 `null`입니다:

```php
use Laravel\Ai\Image;
use Laravel\Ai\Transcription;

Image::of('A donut sitting on the kitchen counter')->generate()->usage->imageOutputTokens;

Transcription::fromPath('/home/laravel/meeting.mp3')->generate()->usage->audioSeconds;
```

<a name="failover"></a>
<!-- ## Failover -->
## Failover

<!-- When prompting or generating other media, you may provide an array of providers / models to automatically failover to a backup provider / model if a service interruption or rate limit is encountered on the primary provider: -->
프롬프트를 보내거나 다른 미디어를 생성할 때 기본 프로바이더에서 서비스 중단이나 사용량 제한을 만나면 백업 프로바이더 / 모델로 자동 장애 조치할 수 있도록 프로바이더 / 모델 배열을 제공할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Image;

$response = (new SalesCoach)->prompt(
    'Analyze this sales transcript...',
    provider: [Lab::OpenAI, Lab::Anthropic],
);

$image = Image::of('A donut sitting on the kitchen counter')
    ->generate(provider: [Lab::Gemini, Lab::xAI]);
```

<!-- Failover only occurs when a `FailoverableException` is thrown — such as a rate limit (`RateLimitedException`), an overloaded or unavailable provider (`ProviderOverloadedException`), or insufficient credits (`InsufficientCreditsException`). Ordinary errors, like a validation or bad request error, will not trigger failover. -->
장애 조치는 `FailoverableException`이 던져질 때만 발생합니다. 예를 들어 사용량 제한(`RateLimitedException`), 과부하 상태이거나 사용할 수 없는 프로바이더(`ProviderOverloadedException`), 크레딧 부족(`InsufficientCreditsException`)이 이에 해당합니다. 검증 오류나 잘못된 요청 오류 같은 일반적인 오류는 장애 조치를 트리거하지 않습니다.

<!-- When you pass a plain list of providers, such as `[Lab::OpenAI, Lab::Anthropic]`, each provider uses its default model. To specify a particular model for each provider in the failover chain, pass an associative array keyed by the provider, using the `Lab` enum's `value` as the key (enum cases cannot be used directly as PHP array keys): -->
`[Lab::OpenAI, Lab::Anthropic]`처럼 프로바이더의 일반 목록을 전달하면 각 프로바이더는 자신의 기본 모델을 사용합니다. 장애 조치 체인의 각 프로바이더에 특정 모델을 지정하려면, `Lab` enum의 `value`를 키로 사용하여 프로바이더별로 키가 지정된 연관 배열을 전달하십시오(enum case는 PHP 배열 키로 직접 사용할 수 없습니다).

```php
use Laravel\Ai\Enums\Lab;

$response = (new SalesCoach)->prompt(
    'Analyze this sales transcript...',
    provider: [
        Lab::Gemini->value => 'gemini-3-flash-preview',
        Lab::DeepSeek->value => 'deepseek-v4-pro',
    ],
);
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- When faking queued image, audio, transcription, or embeddings generation, any `then` callback registered on the queued generation will be invoked with the faked response, allowing you to test the logic contained within the callback. If you would prefer that these callbacks are not invoked, you may fake the queue using `Queue::fake()` as well. -->
큐에 등록된 이미지, 오디오, 전사 또는 임베딩 생성을 페이크하면 해당 생성 작업에 등록된 모든 `then` 콜백이 페이크한 응답과 함께 호출되므로 콜백에 포함된 로직을 테스트할 수 있습니다. 이러한 콜백이 호출되지 않도록 하려면 `Queue::fake()`를 사용해 큐도 페이크할 수 있습니다.

<a name="testing-agents"></a>
<!-- ### Agents -->
### Agents

<!-- To fake an agent's responses during tests, call the `fake` method on the agent class. You may optionally provide an array of responses or a closure: -->
테스트 중에 에이전트의 응답을 가짜로 처리하려면 에이전트 클래스에서 `fake` 메서드를 호출합니다. 선택적으로 응답 배열이나 클로저를 제공할 수 있습니다.

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Prompts\AgentPrompt;

// Automatically generate a fixed response for every prompt...
SalesCoach::fake();

// Provide a list of prompt responses...
SalesCoach::fake([
    'First response',
    'Second response',
]);

// Dynamically handle prompt responses based on the incoming prompt...
SalesCoach::fake(function (AgentPrompt $prompt) {
    return 'Response for: '.$prompt->prompt;
});
```

<!-- When faking an agent that returns structured output, you may provide arrays as responses. The agent will return a structured response containing the given data: -->
구조화된 출력을 반환하는 에이전트를 faking할 때는 배열을 응답으로 제공할 수 있습니다. 에이전트는 주어진 데이터를 포함하는 구조화된 응답을 반환합니다:

```php
SalesCoach::fake([
    ['score' => 87],
]);
```

<!-- You may also fake a response that is awaiting tool approval: -->
도구 승인을 기다리는 응답도 모의할 수 있습니다:

```php
use Laravel\Ai\Approvals\PendingApproval;
use Laravel\Ai\Responses\AgentResponse;

FileAssistant::fake([
    AgentResponse::fakeWithPendingApprovals([
        new PendingApproval(
            id: 'call_abc',
            tool: 'DeleteFile',
            arguments: ['path' => 'invoice.pdf'],
            reason: 'This will permanently delete a file.',
        ),
    ]),
]);

$response = (new FileAssistant)->prompt('Delete the invoice.');

$response->hasPendingApprovals(); // true
```

<!-- In addition, you can fake a response that includes reasoning. The fake emits reasoning events, so the reasoning is reported on streamed runs as well: -->
또한 추론을 포함하는 응답을 모의로 생성할 수 있습니다. 이 모의 응답은 추론 이벤트를 발생시키므로 스트리밍 실행에서도 추론이 함께 보고됩니다:

```php
use Laravel\Ai\Responses\AgentResponse;

SalesCoach::fake([
    AgentResponse::fakeWithReasoning('They asked about pricing.', 'Plans start at $10.'),
]);

$response = (new SalesCoach)->stream('What does it cost?');

foreach ($response as $event) {
    // ...
}

$response->reasoning; // 'They asked about pricing.'
```

> [!NOTE]
> 구조화된 출력을 반환하는 에이전트에서 `Agent::fake()`를 호출했으며 가짜 출력이 명시적으로 제공되지 않았다면, Laravel은 에이전트에 정의된 출력 스키마와 일치하는 가짜 데이터를 자동으로 생성합니다.

<!-- After prompting the agent, you may make assertions about the prompts that were received: -->
에이전트에 프롬프트를 전달한 후에는 수신된 프롬프트에 대해 검증할 수 있습니다.

```php
use Laravel\Ai\Prompts\AgentPrompt;

SalesCoach::assertPrompted('Analyze this...');

SalesCoach::assertPrompted(function (AgentPrompt $prompt) {
    return $prompt->contains('Analyze');
});

SalesCoach::assertPromptedTimes(3);

SalesCoach::assertNotPrompted('Missing prompt');

SalesCoach::assertNeverPrompted();
```

<!-- When asserting an approval continuation, you may inspect the prompt's approval decisions: -->
승인 계속 진행을 검증할 때는 프롬프트의 승인 결정을 검사할 수 있습니다:

```php
use Laravel\Ai\Approvals\Decisions;
use Laravel\Ai\Prompts\AgentPrompt;

FileAssistant::fake();

(new FileAssistant)->prompt(Decisions::from([
    'call_abc' => true,
]));

FileAssistant::assertPrompted(function (AgentPrompt $prompt) {
    return $prompt->hasApprovalDecisions()
        && $prompt->approvalDecisions->get('call_abc')->isApproved();
});
```

<!-- For queued agent invocations, use the queued assertion methods: -->
큐에 등록된 에이전트 호출에는 큐용 검증 메서드를 사용합니다.

```php
use Laravel\Ai\QueuedAgentPrompt;

SalesCoach::assertQueued('Analyze this...');

SalesCoach::assertQueued(function (QueuedAgentPrompt $prompt) {
    return $prompt->contains('Analyze');
});

SalesCoach::assertNotQueued('Missing prompt');

SalesCoach::assertNeverQueued();
```

<!-- To ensure all agent invocations have a corresponding fake response, you may use `preventStrayPrompts`. If an agent is invoked without a defined fake response, an exception will be thrown: -->
모든 에이전트 호출에 대응하는 가짜 응답이 있는지 확인하려면 `preventStrayPrompts`를 사용할 수 있습니다. 정의된 가짜 응답 없이 에이전트가 호출되면 예외가 발생합니다.

```php
SalesCoach::fake()->preventStrayPrompts();
```

<a name="testing-images"></a>
<!-- ### Images -->
### Images

<!-- Image generations may be faked by invoking the `fake` method on the `Image` class. Once image has been faked, various assertions may be performed against the recorded image generation prompts: -->
이미지 생성은 `Image` 클래스에서 `fake` 메서드를 호출하여 가짜로 처리할 수 있습니다. 이미지가 가짜로 처리되면, 기록된 이미지 생성 프롬프트에 대해 다양한 검증을 수행할 수 있습니다.

```php
use Laravel\Ai\Image;
use Laravel\Ai\Prompts\ImagePrompt;
use Laravel\Ai\Prompts\QueuedImagePrompt;

// Automatically generate a fixed response for every prompt...
Image::fake();

// Provide a list of prompt responses...
Image::fake([
    base64_encode($firstImage),
    base64_encode($secondImage),
]);

// Dynamically handle prompt responses based on the incoming prompt...
Image::fake(function (ImagePrompt $prompt) {
    return base64_encode('...');
});
```

<!-- After generating images, you may make assertions about the prompts that were received: -->
이미지를 생성한 후에는 수신된 프롬프트에 대해 검증할 수 있습니다.

```php
Image::assertGenerated(function (ImagePrompt $prompt) {
    return $prompt->contains('sunset') && $prompt->isLandscape();
});

Image::assertNotGenerated('Missing prompt');

Image::assertNothingGenerated();
```

<!-- For queued image generations, use the queued assertion methods: -->
큐에 등록된 이미지 생성에는 큐용 검증 메서드를 사용합니다.

```php
Image::assertQueued(
    fn (QueuedImagePrompt $prompt) => $prompt->contains('sunset')
);

Image::assertNotQueued('Missing prompt');

Image::assertNothingQueued();
```

<!-- To ensure all image generations have a corresponding fake response, you may use `preventStrayImages`. If an image is generated without a defined fake response, an exception will be thrown: -->
모든 이미지 생성에 대응하는 가짜 응답이 있는지 확인하려면 `preventStrayImages`를 사용할 수 있습니다. 정의된 가짜 응답 없이 이미지가 생성되면 예외가 발생합니다.

```php
Image::fake()->preventStrayImages();
```

<a name="testing-audio"></a>
<!-- ### Audio -->
### Audio

<!-- Audio generations may be faked by invoking the `fake` method on the `Audio` class. Once audio has been faked, various assertions may be performed against the recorded audio generation prompts: -->
오디오 생성은 `Audio` 클래스에서 `fake` 메서드를 호출하여 가짜로 처리할 수 있습니다. 오디오가 가짜로 처리되면, 기록된 오디오 생성 프롬프트에 대해 다양한 검증을 수행할 수 있습니다.

```php
use Laravel\Ai\Audio;
use Laravel\Ai\Prompts\AudioPrompt;
use Laravel\Ai\Prompts\QueuedAudioPrompt;

// Automatically generate a fixed response for every prompt...
Audio::fake();

// Provide a list of prompt responses...
Audio::fake([
    base64_encode($firstAudio),
    base64_encode($secondAudio),
]);

// Dynamically handle prompt responses based on the incoming prompt...
Audio::fake(function (AudioPrompt $prompt) {
    return base64_encode('...');
});
```

<!-- After generating audio, you may make assertions about the prompts that were received: -->
오디오를 생성한 후에는 수신된 프롬프트에 대해 검증할 수 있습니다.

```php
Audio::assertGenerated(function (AudioPrompt $prompt) {
    return $prompt->contains('Hello') && $prompt->isFemale();
});

Audio::assertNotGenerated('Missing prompt');

Audio::assertNothingGenerated();
```

<!-- For queued audio generations, use the queued assertion methods: -->
큐에 등록된 오디오 생성에는 큐용 검증 메서드를 사용합니다.

```php
Audio::assertQueued(
    fn (QueuedAudioPrompt $prompt) => $prompt->contains('Hello')
);

Audio::assertNotQueued('Missing prompt');

Audio::assertNothingQueued();
```

<!-- To ensure all audio generations have a corresponding fake response, you may use `preventStrayAudio`. If audio is generated without a defined fake response, an exception will be thrown: -->
모든 오디오 생성에 대응하는 가짜 응답이 있는지 확인하려면 `preventStrayAudio`를 사용할 수 있습니다. 정의된 가짜 응답 없이 오디오가 생성되면 예외가 발생합니다.

```php
Audio::fake()->preventStrayAudio();
```

<a name="testing-transcriptions"></a>
<!-- ### Transcriptions -->
### Transcriptions

<!-- Transcription generations may be faked by invoking the `fake` method on the `Transcription` class. Once transcription has been faked, various assertions may be performed against the recorded transcription generation prompts: -->
전사 생성은 `Transcription` 클래스에서 `fake` 메서드를 호출하여 가짜로 처리할 수 있습니다. 전사가 가짜로 처리되면, 기록된 전사 생성 프롬프트에 대해 다양한 검증을 수행할 수 있습니다.

```php
use Laravel\Ai\Transcription;
use Laravel\Ai\Prompts\TranscriptionPrompt;
use Laravel\Ai\Prompts\QueuedTranscriptionPrompt;

// Automatically generate a fixed response for every prompt...
Transcription::fake();

// Provide a list of prompt responses...
Transcription::fake([
    'First transcription text.',
    'Second transcription text.',
]);

// Dynamically handle prompt responses based on the incoming prompt...
Transcription::fake(function (TranscriptionPrompt $prompt) {
    return 'Transcribed text...';
});
```

<!-- After generating transcriptions, you may make assertions about the prompts that were received: -->
전사를 생성한 후에는 수신된 프롬프트에 대해 검증할 수 있습니다.

```php
Transcription::assertGenerated(function (TranscriptionPrompt $prompt) {
    return $prompt->language === 'en' && $prompt->isDiarized();
});

Transcription::assertNotGenerated(
    fn (TranscriptionPrompt $prompt) => $prompt->language === 'fr'
);

Transcription::assertNothingGenerated();
```

<!-- For queued transcription generations, use the queued assertion methods: -->
큐에 등록된 전사 생성에는 큐용 검증 메서드를 사용합니다.

```php
Transcription::assertQueued(
    fn (QueuedTranscriptionPrompt $prompt) => $prompt->isDiarized()
);

Transcription::assertNotQueued(
    fn (QueuedTranscriptionPrompt $prompt) => $prompt->language === 'fr'
);

Transcription::assertNothingQueued();
```

<!-- To ensure all transcription generations have a corresponding fake response, you may use `preventStrayTranscriptions`. If a transcription is generated without a defined fake response, an exception will be thrown: -->
모든 전사 생성에 대응하는 가짜 응답이 있는지 확인하려면 `preventStrayTranscriptions`를 사용할 수 있습니다. 정의된 가짜 응답 없이 전사가 생성되면 예외가 발생합니다.

```php
Transcription::fake()->preventStrayTranscriptions();
```

<a name="testing-embeddings"></a>
<!-- ### Embeddings -->
### Embeddings

<!-- Embeddings generations may be faked by invoking the `fake` method on the `Embeddings` class. Once embeddings has been faked, various assertions may be performed against the recorded embeddings generation prompts: -->
임베딩 생성은 `Embeddings` 클래스에서 `fake` 메서드를 호출하여 가짜로 처리할 수 있습니다. 임베딩이 가짜로 처리되면, 기록된 임베딩 생성 프롬프트에 대해 다양한 검증을 수행할 수 있습니다.

```php
use Laravel\Ai\Embeddings;
use Laravel\Ai\Prompts\EmbeddingsPrompt;
use Laravel\Ai\Prompts\QueuedEmbeddingsPrompt;

// Automatically generate fake embeddings of the proper dimensions for every prompt...
Embeddings::fake();

// Provide a list of prompt responses...
Embeddings::fake([
    [$firstEmbeddingVector],
    [$secondEmbeddingVector],
]);

// Dynamically handle prompt responses based on the incoming prompt...
Embeddings::fake(function (EmbeddingsPrompt $prompt) {
    return array_map(
        fn () => Embeddings::fakeEmbedding($prompt->dimensions),
        $prompt->inputs
    );
});
```

<!-- After generating embeddings, you may make assertions about the prompts that were received: -->
임베딩을 생성한 후에는 수신된 프롬프트에 대해 검증할 수 있습니다.

```php
Embeddings::assertGenerated(function (EmbeddingsPrompt $prompt) {
    return $prompt->contains('Laravel') && $prompt->dimensions === 1536;
});

Embeddings::assertNotGenerated(
    fn (EmbeddingsPrompt $prompt) => $prompt->contains('Other')
);

Embeddings::assertNothingGenerated();
```

<!-- For queued embeddings generations, use the queued assertion methods: -->
큐에 등록된 임베딩 생성에는 큐용 검증 메서드를 사용합니다.

```php
Embeddings::assertQueued(
    fn (QueuedEmbeddingsPrompt $prompt) => $prompt->contains('Laravel')
);

Embeddings::assertNotQueued(
    fn (QueuedEmbeddingsPrompt $prompt) => $prompt->contains('Other')
);

Embeddings::assertNothingQueued();
```

<!-- To ensure all embeddings generations have a corresponding fake response, you may use `preventStrayEmbeddings`. If embeddings are generated without a defined fake response, an exception will be thrown: -->
모든 임베딩 생성에 대응하는 가짜 응답이 있는지 확인하려면 `preventStrayEmbeddings`를 사용할 수 있습니다. 정의된 가짜 응답 없이 임베딩이 생성되면 예외가 발생합니다.

```php
Embeddings::fake()->preventStrayEmbeddings();
```

<a name="testing-reranking"></a>
<!-- ### Reranking -->
### Reranking

<!-- Reranking operations may be faked by invoking the `fake` method on the `Reranking` class: -->
재순위화 작업은 `Reranking` 클래스에서 `fake` 메서드를 호출하여 가짜로 처리할 수 있습니다.

```php
use Laravel\Ai\Reranking;
use Laravel\Ai\Prompts\RerankingPrompt;
use Laravel\Ai\Responses\Data\RankedDocument;

// Automatically generate a fake reranked responses...
Reranking::fake();

// Provide custom responses...
Reranking::fake([
    [
        new RankedDocument(index: 0, document: 'First', score: 0.95),
        new RankedDocument(index: 1, document: 'Second', score: 0.80),
    ],
]);
```

<!-- After reranking, you may make assertions about the operations that were performed: -->
재순위화한 후에는 실행된 작업에 대해 검증할 수 있습니다.

```php
Reranking::assertReranked(function (RerankingPrompt $prompt) {
    return $prompt->contains('Laravel') && $prompt->limit === 5;
});

Reranking::assertNotReranked(
    fn (RerankingPrompt $prompt) => $prompt->contains('Django')
);

Reranking::assertNothingReranked();
```

<a name="testing-classification"></a>
<!-- ### Classification -->
### Classification

<!-- Classification may be faked by invoking the `fake` method on the `Classification` class. If no custom responses are provided, Laravel will automatically generate answers that match the shape of each question: -->
`Classification` 클래스에서 `fake` 메서드를 호출하면 Classification을 가짜로 처리할 수 있습니다. 사용자 지정 응답을 제공하지 않으면 Laravel은 각 질문의 형식에 맞는 답변을 자동으로 생성합니다:

```php
use Laravel\Ai\Classification;
use Laravel\Ai\Prompts\ClassificationPrompt;
use Laravel\Ai\Responses\Data\BooleanAnswer;
use Laravel\Ai\Responses\Data\ChoiceAnswer;

// Automatically generate fake answers...
Classification::fake();

// Provide answers for specific questions...
Classification::fake([
    [
        'urgent' => new BooleanAnswer(0.94),
        'department' => new ChoiceAnswer('technical', [
            'billing' => 0.08,
            'technical' => 0.87,
            'sales' => 0.05,
        ], confidence: 0.82),
    ],
]);

// Build answers from the prompt...
Classification::fake(fn (ClassificationPrompt $prompt) => [
    'urgent' => new BooleanAnswer($prompt->contains('ASAP') ? 1.0 : 0.0),
]);
```

<!-- Questions that are omitted from a fake response will still receive a generated answer, so your tests only need to provide the answers they make assertions against. -->
가짜 응답에서 생략한 질문에도 생성된 답변이 제공되므로, 테스트에서는 단언할 답변만 제공하면 됩니다.

<!-- After classifying, you may make assertions about the operations that were performed: -->
분류한 후에는 수행된 작업에 대해 어설션할 수 있습니다:

```php
Classification::assertClassified(function (ClassificationPrompt $prompt) {
    return $prompt->contains('refund') && $prompt->asks('department');
});

Classification::assertNotClassified(
    fn (ClassificationPrompt $prompt) => $prompt->asks('sentiment')
);

Classification::assertNothingClassified();
```

<a name="testing-files"></a>
<!-- ### Files -->
### Files

<!-- File operations may be faked by invoking the `fake` method on the `Files` class: -->
파일 작업은 `Files` 클래스에서 `fake` 메서드를 호출하여 가짜로 처리할 수 있습니다.

```php
use Laravel\Ai\Files;

Files::fake();
```

<!-- Once file operations have been faked, you may make assertions about the uploads and deletions that occurred: -->
파일 작업이 가짜로 처리되면, 발생한 업로드와 삭제에 대해 검증할 수 있습니다.

```php
use Laravel\Ai\Contracts\Files\StorableFile;
use Laravel\Ai\Files\Document;

// Store files...
Document::fromString('Hello, Laravel!', mimeType: 'text/plain')
    ->as('hello.txt')
    ->put();

// Make assertions...
Files::assertStored(fn (StorableFile $file) =>
    (string) $file === 'Hello, Laravel!' &&
        $file->mimeType() === 'text/plain'
);

Files::assertNotStored(fn (StorableFile $file) =>
    (string) $file === 'Hello, World!'
);

Files::assertNothingStored();
```

<!-- For asserting against file deletions, you may pass a file ID: -->
파일 삭제를 검증하려면 파일 ID를 전달할 수 있습니다.

```php
Files::assertDeleted('file-id');
Files::assertNotDeleted('file-id');
Files::assertNothingDeleted();
```

<a name="testing-vector-stores"></a>
<!-- ### Vector Stores -->
### Vector Stores

<!-- Vector store operations may be faked by invoking the `fake` method on the `Stores` class. Faking stores will also fake [file operations](#files) automatically: -->
벡터 스토어 작업은 `Stores` 클래스에서 `fake` 메서드를 호출하여 가짜로 처리할 수 있습니다. 스토어를 가짜로 처리하면 [file operations](#files)도 자동으로 가짜 처리됩니다.

```php
use Laravel\Ai\Stores;

Stores::fake();
```

<!-- Once store operations have been faked, you may make assertions about the stores that were created or deleted: -->
스토어 작업이 가짜로 처리되면, 생성되거나 삭제된 스토어에 대해 검증할 수 있습니다.

```php
use Laravel\Ai\Stores;

// Create store...
$store = Stores::create('Knowledge Base');

// Make assertions...
Stores::assertCreated('Knowledge Base');

Stores::assertCreated(fn (string $name, ?string $description) =>
    $name === 'Knowledge Base'
);

Stores::assertNotCreated('Other Store');

Stores::assertNothingCreated();
```

<!-- For asserting against store deletions, you may provide the store ID: -->
저장소 삭제를 어설션하려면 저장소 ID를 제공할 수 있습니다:

```php
Stores::assertDeleted('store_id');
Stores::assertNotDeleted('other_store_id');
Stores::assertNothingDeleted();
```

<!-- To assert files were added or removed from a store, use the assertion methods on a given `Store` instance: -->
저장소에 파일이 추가되었거나 제거되었는지 어설션하려면, 지정된 `Store` 인스턴스의 어설션 메서드를 사용합니다:

```php
Stores::fake();

$store = Stores::get('store_id');

// Add / remove files...
$store->add('added_id');
$store->remove('removed_id');

// Make assertions...
$store->assertAdded('added_id');
$store->assertRemoved('removed_id');

$store->assertNotAdded('other_file_id');
$store->assertNotRemoved('other_file_id');
```

<!-- If a file is stored in the provider's [file storage](#files) and added to a vector store in the same request, you may not know the file's provider ID. In this case, you can pass a closure to the `assertAdded` method to assert against the content of the added file: -->
파일이 프로바이더의 [file storage](#files)에 저장되고 같은 요청에서 벡터 스토어에 추가되는 경우, 해당 파일의 프로바이더 ID를 알 수 없을 수 있습니다. 이 경우 `assertAdded` 메서드에 클로저를 전달하여 추가된 파일의 내용에 대해 어설션할 수 있습니다:

```php
use Laravel\Ai\Contracts\Files\StorableFile;
use Laravel\Ai\Files\Document;

$store->add(Document::fromString('Hello, World!', 'text/plain')->as('hello.txt'));

$store->assertAdded(fn (StorableFile $file) => $file->name() === 'hello.txt');
$store->assertAdded(fn (StorableFile $file) => $file->content() === 'Hello, World!');
```

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- The Laravel AI SDK dispatches a variety of [events](/docs/13.x/events), including: -->
Laravel AI SDK는 다음을 비롯한 다양한 [events](/docs/13.x/events)를 디스패치합니다:

- `AddingFileToStore`
- `AgentFailed`
- `AgentFailedOver`
- `AgentPrompted`
- `AgentStreamed`
- `AudioGenerated`
- `Classified`
- `Classifying`
- `CreatingStore`
- `EmbeddingsGenerated`
- `FileAddedToStore`
- `FileDeleted`
- `FileRemovedFromStore`
- `FileStored`
- `GeneratingAudio`
- `GeneratingEmbeddings`
- `GeneratingImage`
- `GeneratingTranscription`
- `ImageGenerated`
- `InvokingTool`
- `PromptingAgent`
- `ProviderFailedOver`
- `RemovingFileFromStore`
- `Reranked`
- `Reranking`
- `StartingStep`
- `StepCompleted`
- `StepFailed`
- `StoreCreated`
- `StoreDeleted`
- `StoringFile`
- `StreamingAgent`
- `ToolApprovalRequested`
- `ToolApprovalResolved`
- `ToolFailed`
- `ToolInvoked`
- `TranscriptionGenerated`

<!-- You can listen to any of these events to log or store AI SDK usage information. -->
이 이벤트 중 어느 것이든 리스닝하여 AI SDK 사용 정보를 로그로 남기거나 저장할 수 있습니다.
