<!-- # Laravel AI SDK -->
# Laravel AI SDK

- [Introduction](#introduction)
- [Installation](#installation)
    - [Configuration](#configuration)
    - [Custom Base URLs](#custom-base-urls)
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
    - [MCP Tools](#mcp-tools)
    - [Provider Tools](#provider-tools)
    - [Sub-Agents](#sub-agents)
    - [Middleware](#middleware)
    - [Anonymous Agents](#anonymous-agents)
    - [Agent Configuration](#agent-configuration)
    - [Provider Options](#provider-options)
- [Images](#images)
- [Audio (TTS)](#audio)
- [Transcription (STT)](#transcription)
- [Embeddings](#embeddings)
    - [Querying Embeddings](#querying-embeddings)
    - [Caching Embeddings](#caching-embeddings)
- [Reranking](#reranking)
- [Files](#files)
- [Vector Stores](#vector-stores)
    - [Adding Files to Stores](#adding-files-to-stores)
- [Failover](#failover)
- [Testing](#testing)
    - [Agents](#testing-agents)
    - [Images](#testing-images)
    - [Audio](#testing-audio)
    - [Transcriptions](#testing-transcriptions)
    - [Embeddings](#testing-embeddings)
    - [Reranking](#testing-reranking)
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
OPENROUTER_API_KEY=
JINA_API_KEY=
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

<a name="provider-support"></a>
<!-- ### Provider Support -->
### Provider Support

<!-- The AI SDK supports a variety of providers across its features. The following table summarizes which providers are available for each feature: -->
AI SDK는 다양한 기능에서 여러 프로바이더를 지원합니다. 다음 표는 각 기능에서 사용할 수 있는 프로바이더를 요약한 것입니다.

| 기능 | 프로바이더 |
|---|---|
| 텍스트 | OpenAI, Anthropic, Gemini, Azure, Bedrock, Groq, xAI, DeepSeek, Mistral, Ollama, OpenRouter |
| 이미지 | OpenAI, Gemini, xAI, Azure, Bedrock, OpenRouter |
| TTS | OpenAI, ElevenLabs, Gemini |
| STT | OpenAI, ElevenLabs, Mistral, Gemini |
| 임베딩 | OpenAI, Gemini, Azure, Bedrock, Cohere, Mistral, Jina, VoyageAI, Ollama, OpenRouter |
| 재순위 지정 | Cohere, Jina, VoyageAI |
| 파일 | OpenAI, Anthropic, Gemini |

<!-- The `Laravel\Ai\Enums\Lab` enum may be used to reference providers throughout your code instead of using plain strings: -->
코드 전체에서 일반 문자열 대신 `Laravel\Ai\Enums\Lab` enum을 사용하여 프로바이더를 참조할 수 있습니다.

```php
use Laravel\Ai\Enums\Lab;

Lab::Anthropic;
Lab::OpenAI;
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
    model: 'claude-haiku-4-5-20251001',
    timeout: 120,
);
```

<a name="conversation-context"></a>
<!-- ### Conversation Context -->
### Conversation Context

<!-- If your agent implements the `Conversational` interface, you may use the `messages` method to return the previous conversation context, if applicable: -->
에이전트가 `Conversational` 인터페이스를 구현하는 경우, 해당된다면 `messages` 메서드를 사용하여 이전 대화 컨텍스트를 반환할 수 있습니다.

```php
use App\Models\History;
use Laravel\Ai\Messages\Message;

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
```

<a name="remembering-conversations"></a>
<!-- #### Remembering Conversations -->
#### Remembering Conversations

> **참고:** `RemembersConversations` trait를 사용하기 전에 `vendor:publish` Artisan 명령어를 사용하여 AI SDK 마이그레이션을 게시하고 실행해야 합니다. 이 마이그레이션은 대화를 저장하는 데 필요한 데이터베이스 테이블을 생성합니다.

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

<!-- When using the `RemembersConversations` trait, previous messages are automatically loaded and included in the conversation context when prompting. New messages (both user and assistant) are automatically stored after each interaction. -->
`RemembersConversations` trait를 사용할 때는 프롬프트할 때 이전 메시지가 자동으로 로드되어 대화 컨텍스트에 포함됩니다. 새 메시지(사용자와 어시스턴트 모두)는 각 상호작용 후 자동으로 저장됩니다.

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
        Files\Document::fromStorage('transcript.pdf') // Attach a document from a filesystem disk...
        Files\Document::fromPath('/home/laravel/transcript.md') // Attach a document from a local path...
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
        Files\Image::fromStorage('photo.jpg') // Attach an image from a filesystem disk...
        Files\Image::fromPath('/home/laravel/photo.jpg') // Attach an image from a local path...
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

<a name="streaming-using-the-vercel-ai-sdk-protocol"></a>
<!-- #### Streaming Using the Vercel AI SDK Protocol -->
#### Streaming Using the Vercel AI SDK Protocol

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
    'Analyze this sales transcript...'
    new Channel('channel-name'),
);
```

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

<a name="mcp-tools"></a>
<!-- ### MCP Tools -->
### MCP Tools

<!-- If your application uses [Laravel MCP](/docs/13.x/mcp), you may give your agents tools exposed by [Model Context Protocol](https://modelcontextprotocol.io) servers. Using the [Laravel MCP client](/docs/13.x/mcp#client), you may connect to a remote or local MCP server and pass its tools directly to your agent. -->
애플리케이션에서 [Laravel MCP](/docs/13.x/mcp)를 사용한다면, [Model Context Protocol](https://modelcontextprotocol.io) 서버가 노출하는 도구를 에이전트에 제공할 수 있습니다. [Laravel MCP client](/docs/13.x/mcp#client)를 사용하면 원격 또는 로컬 MCP 서버에 연결하여 해당 도구를 에이전트에 직접 전달할 수 있습니다.

> [!NOTE]
> MCP 도구를 사용하려면 애플리케이션에 [Laravel MCP](/docs/13.x/mcp) 패키지가 설치되어 있어야 합니다.

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
AI SDK는 각 MCP 도구를 자동으로 래핑하므로 에이전트가 다른 도구와 마찬가지로 호출할 수 있습니다. [named MCP client](/docs/13.x/mcp#named-clients)를 사용할 수도 있습니다.

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
또는 [local MCP server](/docs/13.x/mcp#client-connecting)에 연결할 수도 있습니다.

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
베어러 토큰과 OAuth를 포함하여 MCP 클라이언트를 생성하고 인증하는 방법에 대한 자세한 내용은 [MCP client documentation](/docs/13.x/mcp#client)를 참고하십시오.

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

<!-- **Supported Providers:** Anthropic, OpenAI, Gemini -->
**지원 제공자:** Anthropic, OpenAI, Gemini

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

<!-- **Supported providers:** Anthropic, Gemini -->
**지원 제공자:** Anthropic, Gemini

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

<!-- **Supported providers:** OpenAI, Gemini -->
**지원 제공자:** OpenAI, Gemini

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
<?php

namespace App\Ai\Agents;

use App\Ai\Tools\LookupOrder;
use Laravel\Ai\Attributes\Provider;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\CanActAsTool;
use Laravel\Ai\Contracts\HasTools;
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Promptable;

#[Provider(Lab::Anthropic)]
class RefundsAgent implements Agent, CanActAsTool, HasTools
{
    use Promptable;

    /**
     * Get the instructions that the agent should follow.
     */
    public function instructions(): string
    {
        return 'You are a refunds specialist. Use order details and the refund policy to give concise eligibility guidance.';
    }

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

    /**
     * Get the tools available to the agent.
     *
     * @return Tool[]
     */
    public function tools(): iterable
    {
        return [
            new LookupOrder,
        ];
    }
}
```

<!-- If a sub-agent does not implement `CanActAsTool`, Laravel will use the agent's class basename as the tool name and a generic description that asks the parent agent to pass a clear, self-contained task description. Each sub-agent invocation runs in isolation and does not receive the parent agent's conversation history. -->
하위 에이전트가 `CanActAsTool`을 구현하지 않으면 Laravel은 에이전트 클래스의 basename을 툴 이름으로 사용하고, 부모 에이전트가 명확하고 독립적인 작업 설명을 전달하도록 요청하는 기본 설명을 사용합니다. 각 하위 에이전트 호출은 격리되어 실행되며 부모 에이전트의 대화 기록을 받지 않습니다.

<a name="middleware"></a>
<!-- ### Middleware -->
### Middleware
<!-- Agents support middleware, allowing you to intercept and modify prompts before they are sent to the provider. Middleware can be created using the `make:agent-middleware` Artisan command: -->
Agents는 Middleware를 지원하므로, 프롬프트가 provider로 전송되기 전에 이를 가로채고 수정할 수 있습니다. Middleware는 `make:agent-middleware` Artisan 명령어로 만들 수 있습니다.

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

<!-- Each middleware class should define a `handle` method that receives the `AgentPrompt` and a `Closure` to pass the prompt to the next middleware: -->
각 Middleware 클래스는 `AgentPrompt`와 프롬프트를 다음 Middleware로 전달하기 위한 `Closure`를 받는 `handle` 메서드를 정의해야 합니다.

```php
<?php

namespace App\Ai\Middleware;

use Closure;
use Laravel\Ai\Prompts\AgentPrompt;

class LogPrompts
{
    /**
     * Handle the incoming prompt.
     */
    public function handle(AgentPrompt $prompt, Closure $next)
    {
        Log::info('Prompting agent', ['prompt' => $prompt->prompt]);

        return $next($prompt);
    }
}
```

<!-- You may use the `then` method on the response to execute code after the agent has finished processing. This works for both synchronous and streaming responses: -->
에이전트가 처리를 완료한 뒤 코드를 실행하려면 응답에서 `then` 메서드를 사용할 수 있습니다. 이 방식은 동기 응답과 스트리밍 응답 모두에서 동작합니다.

```php
public function handle(AgentPrompt $prompt, Closure $next)
{
    return $next($prompt)->then(function (AgentResponse $response) {
        Log::info('Agent responded', ['text' => $response->text]);
    });
}
```

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
)->prompt('Tell me about Laravel')
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
)->prompt('Generate a random number less than 100')
```

<a name="agent-configuration"></a>
<!-- ### Agent Configuration -->
### Agent Configuration

<!-- You may configure text generation options for an agent using PHP attributes. The following attributes are available: -->
PHP 속성을 사용하여 에이전트의 텍스트 생성 옵션을 설정할 수 있습니다. 사용할 수 있는 속성은 다음과 같습니다.

<!--
- `MaxSteps`: The maximum number of steps the agent may take when using tools.
- `MaxTokens`: The maximum number of tokens the model may generate.
- `Model`: The model the agent should use.
- `Provider`: The AI provider (or providers for failover) to use for the agent.
- `Temperature`: The sampling temperature to use for generation (0.0 to 1.0).
- `Timeout`: The HTTP timeout in seconds for agent requests (default: 60).
- `TopP`: The nucleus sampling probability to use for generation (0.0 to 1.0).
- `UseCheapestModel`: Use the provider's cheapest text model for cost optimization.
- `UseSmartestModel`: Use the provider's most capable text model for complex tasks.
-->
- `MaxSteps`: 툴을 사용할 때 에이전트가 수행할 수 있는 최대 단계 수입니다.
- `MaxTokens`: 모델이 생성할 수 있는 최대 토큰 수입니다.
- `Model`: 에이전트가 사용할 모델입니다.
- `Provider`: 에이전트가 사용할 AI 프로바이더입니다. failover를 위해 여러 프로바이더를 지정할 수도 있습니다.
- `Temperature`: 생성에 사용할 샘플링 온도입니다(0.0부터 1.0까지).
- `Timeout`: 에이전트 요청의 HTTP 제한 시간(초)입니다(기본값: 60).
- `TopP`: 생성에 사용할 뉴클리어스 샘플링 확률입니다(0.0부터 1.0까지).
- `UseCheapestModel`: 비용 최적화를 위해 프로바이더의 가장 저렴한 텍스트 모델을 사용합니다.
- `UseSmartestModel`: 복잡한 작업을 위해 프로바이더의 가장 성능이 뛰어난 텍스트 모델을 사용합니다.

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
#[Model('claude-haiku-4-5-20251001')]
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
> `UseCheapestModel`과 `UseSmartestModel`이 선택하는 기본 모델은 프로바이더가 새 모델을 출시함에 따라 Laravel AI SDK 릴리스마다 달라질 수 있습니다. 모델이 바뀌면 동작 변화, 더 이상 사용되지 않는 매개변수, 상당한 비용 차이가 발생할 수 있습니다. 안정적이고 예측 가능한 모델과 가격이 필요하다면 `Model` 속성을 사용하여 모델을 명시적으로 지정하십시오.

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

<!-- The Anthropic example above also enables [prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) via `cache_control`. -->
위 Anthropic 예시는 `cache_control`을 통해 [prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)도 활성화합니다.

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

<a name="querying-embeddings"></a>
<!-- ### Querying Embeddings -->
### Querying Embeddings

<!-- Once you have generated embeddings, you will typically store them in a `vector` column in your database for later querying. Laravel provides native support for vector columns on PostgreSQL via the `pgvector` extension. To get started, define a `vector` column in your migration, specifying the number of dimensions: -->
임베딩을 생성한 뒤에는 보통 나중에 쿼리할 수 있도록 데이터베이스의 `vector` 컬럼에 저장합니다. Laravel은 `pgvector` 확장을 통해 PostgreSQL의 벡터 컬럼을 네이티브로 지원합니다. 시작하려면 마이그레이션에서 차원 수를 지정하여 `vector` 컬럼을 정의합니다:

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

<!-- On your Eloquent model, you should cast the vector column to an `array`: -->
Eloquent 모델에서는 벡터 컬럼을 `array`로 casting해야 합니다:

```php
protected function casts(): array
{
    return [
        'embedding' => 'array',
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
> 벡터 쿼리는 현재 `pgvector` 확장을 사용하는 PostgreSQL 연결에서만 지원됩니다.

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
        // ...
    ],
],
```

<!-- When caching is enabled, embeddings are cached for 30 days. The cache key is based on the provider, model, dimensions, and input content, ensuring that identical requests return cached results while different configurations generate fresh embeddings. -->
캐싱이 활성화되면 임베딩은 30일 동안 캐시됩니다. 캐시 키는 프로바이더, 모델, 차원 수, 입력 내용을 기반으로 생성되므로, 동일한 요청은 캐시된 결과를 반환하고 설정이 다른 요청은 새 임베딩을 생성합니다.

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

<!-- The `limit` method may be used to restrict the number of results returned: -->
`limit` 메서드를 사용하여 반환되는 결과 수를 제한할 수 있습니다:

```php
$response = Reranking::of($documents)
    ->limit(5)
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
    provider: Lab::Cohere
);
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
    'Analyze the attached sales transcript...'
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
벡터 저장소를 사용하면 검색 증강 생성(RAG)에 사용할 수 있는 검색 가능한 파일 컬렉션을 만들 수 있습니다. `Laravel\Ai\Stores` 클래스는 벡터 저장소를 생성하고, 가져오고, 삭제하는 메서드를 제공합니다:

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
기존 벡터 저장소를 ID로 가져오려면 `get` 메서드를 사용합니다:

```php
use Laravel\Ai\Stores;

$store = Stores::get('store_id');

$store->id;
$store->name;
$store->fileCounts;
$store->ready;
```

<!-- To delete a vector store, use the `delete` method on the `Stores` class or the store instance: -->
벡터 저장소를 삭제하려면 `Stores` 클래스 또는 저장소 인스턴스에서 `delete` 메서드를 사용합니다:

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
벡터 저장소가 준비되면 `add` 메서드를 사용하여 [files](#files)을 추가할 수 있습니다. 저장소에 추가된 파일은 [file search provider tool](#file-search)를 사용한 의미 검색을 위해 자동으로 인덱싱됩니다:

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

> **참고:** 일반적으로 이전에 저장한 파일을 벡터 저장소에 추가하면 반환되는 문서 ID는 파일에 이미 할당된 ID와 일치합니다. 그러나 일부 벡터 저장소 프로바이더는 새롭고 다른 "문서 ID"를 반환할 수 있습니다. 따라서 나중에 참조할 수 있도록 두 ID를 모두 데이터베이스에 저장하는 것이 좋습니다.

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
벡터 저장소에서 파일을 제거해도 프로바이더의 [file storage](#files)에서는 제거되지 않습니다. 벡터 저장소에서 파일을 제거하고 파일 저장소에서도 영구적으로 삭제하려면 `deleteFile` 인수를 사용합니다:

```php
$store->remove('file_abc123', deleteFile: true);
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

> **참고:** 구조화된 출력을 반환하는 에이전트에서 `Agent::fake()`가 호출되면, Laravel은 에이전트에 정의된 출력 스키마와 일치하는 가짜 데이터를 자동으로 생성합니다.

<!-- After prompting the agent, you may make assertions about the prompts that were received: -->
에이전트에 프롬프트를 전달한 후에는 수신된 프롬프트에 대해 검증할 수 있습니다.

```php
use Laravel\Ai\Prompts\AgentPrompt;

SalesCoach::assertPrompted('Analyze this...');

SalesCoach::assertPrompted(function (AgentPrompt $prompt) {
    return $prompt->contains('Analyze');
});

SalesCoach::assertNotPrompted('Missing prompt');

SalesCoach::assertNeverPrompted();
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
재순위화를 수행한 후에는 실행된 작업에 대해 검증할 수 있습니다.

```php
Reranking::assertReranked(function (RerankingPrompt $prompt) {
    return $prompt->contains('Laravel') && $prompt->limit === 5;
});

Reranking::assertNotReranked(
    fn (RerankingPrompt $prompt) => $prompt->contains('Django')
);

Reranking::assertNothingReranked();
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
        $file->mimeType() === 'text/plain';
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
파일이 프로바이더의 [file storage](#files)에 저장되고 같은 요청에서 벡터 저장소에 추가되는 경우, 해당 파일의 프로바이더 ID를 알 수 없을 수 있습니다. 이 경우 `assertAdded` 메서드에 클로저를 전달하여 추가된 파일의 내용에 대해 어설션할 수 있습니다:

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
Laravel AI SDK는 다음을 포함한 다양한 [events](/docs/13.x/events)를 디스패치합니다:

<!--
- `AddingFileToStore`
- `AgentPrompted`
- `AgentStreamed`
- `AudioGenerated`
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
- `RemovingFileFromStore`
- `Reranked`
- `Reranking`
- `StoreCreated`
- `StoringFile`
- `StreamingAgent`
- `ToolInvoked`
- `TranscriptionGenerated`
-->
- `AddingFileToStore`
- `AgentPrompted`
- `AgentStreamed`
- `AudioGenerated`
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
- `RemovingFileFromStore`
- `Reranked`
- `Reranking`
- `StoreCreated`
- `StoringFile`
- `StreamingAgent`
- `ToolInvoked`
- `TranscriptionGenerated`

<!-- You can listen to any of these events to log or store AI SDK usage information. -->
이 이벤트 중 어느 것이든 리스닝하여 AI SDK 사용 정보를 로그로 남기거나 저장할 수 있습니다.
