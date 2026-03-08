# Laravel AI SDK

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [사용자 지정 Base URL](#custom-base-urls)
    - [Provider 지원](#provider-support)
- [Agents](#agents)
    - [프롬프트](#prompting)
    - [대화 컨텍스트](#conversation-context)
    - [구조화된 출력](#structured-output)
    - [첨부 파일](#attachments)
    - [스트리밍](#streaming)
    - [브로드캐스팅](#broadcasting)
    - [큐 처리](#queueing)
    - [Tools](#tools)
    - [Provider Tools](#provider-tools)
    - [미들웨어](#middleware)
    - [익명 Agent](#anonymous-agents)
    - [Agent 설정](#agent-configuration)
- [이미지](#images)
- [오디오 (TTS)](#audio)
- [전사 (STT)](#transcription)
- [임베딩](#embeddings)
    - [임베딩 조회](#querying-embeddings)
    - [임베딩 캐싱](#caching-embeddings)
- [리랭킹](#reranking)
- [파일](#files)
- [벡터 스토어](#vector-stores)
    - [스토어에 파일 추가](#adding-files-to-stores)
- [Failover](#failover)
- [테스트](#testing)
    - [Agents](#testing-agents)
    - [이미지](#testing-images)
    - [오디오](#testing-audio)
    - [전사](#testing-transcriptions)
    - [임베딩](#testing-embeddings)
    - [리랭킹](#testing-reranking)
    - [파일](#testing-files)
    - [벡터 스토어](#testing-vector-stores)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel AI SDK](https://github.com/laravel/ai)는 OpenAI, Anthropic, Gemini 등 다양한 AI provider와 상호작용하기 위한 통합되고 표현력이 뛰어난 API를 제공합니다.  

AI SDK를 사용하면 tools와 구조화된 출력(Structured Output)을 갖춘 지능형 agent를 만들고, 이미지를 생성하고, 오디오를 합성 및 전사하고, 벡터 임베딩을 생성하는 등 다양한 작업을 수행할 수 있습니다. 이 모든 작업을 Laravel에 친화적인 일관된 인터페이스로 사용할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

Composer를 사용하여 Laravel AI SDK를 설치할 수 있습니다.

```shell
composer require laravel/ai
```

다음으로 `vendor:publish` Artisan 명령어를 사용하여 AI SDK 설정 파일과 migration 파일을 퍼블리시해야 합니다.

```shell
php artisan vendor:publish --provider="Laravel\Ai\AiServiceProvider"
```

마지막으로 애플리케이션의 데이터베이스 migration을 실행합니다.  
이 과정에서 AI SDK가 대화 기록을 저장하기 위해 사용하는 `agent_conversations` 및 `agent_conversation_messages` 테이블이 생성됩니다.

```shell
php artisan migrate
```

<a name="configuration"></a>
### 설정

애플리케이션의 `config/ai.php` 설정 파일 또는 `.env` 파일에서 AI provider 인증 정보를 정의할 수 있습니다.

```ini
ANTHROPIC_API_KEY=
COHERE_API_KEY=
ELEVENLABS_API_KEY=
GEMINI_API_KEY=
MISTRAL_API_KEY=
OLLAMA_API_KEY=
OPENAI_API_KEY=
JINA_API_KEY=
VOYAGEAI_API_KEY=
XAI_API_KEY=
```

텍스트, 이미지, 오디오, 전사, 임베딩 등에 사용되는 기본 모델 역시 `config/ai.php` 설정 파일에서 지정할 수 있습니다.

<a name="custom-base-urls"></a>
### 사용자 지정 Base URLs

기본적으로 Laravel AI SDK는 각 provider의 공개 API 엔드포인트에 직접 연결합니다.  

하지만 다음과 같은 상황에서는 다른 엔드포인트를 통해 요청을 전달해야 할 수도 있습니다.

- API 키 관리를 중앙화하기 위해 프록시 서비스를 사용하는 경우
- rate limiting을 구현하는 경우
- 기업 내부 게이트웨이를 통해 트래픽을 라우팅해야 하는 경우

이러한 경우 provider 설정에 `url` 파라미터를 추가하여 사용자 지정 base URL을 설정할 수 있습니다.

```php
'providers' => [
    'openai' => [
        'driver' => 'openai',
        'key' => env('OPENAI_API_KEY'),
        'url' => env('OPENAI_BASE_URL'),
    ],

    'anthropic' => [
        'driver' => 'anthropic',
        'key' => env('ANTHROPIC_API_KEY'),
        'url' => env('ANTHROPIC_BASE_URL'),
    ],
],
```

이 기능은 LiteLLM이나 Azure OpenAI Gateway 같은 프록시 서비스를 사용하는 경우 또는 대체 API 엔드포인트를 사용하는 경우에 유용합니다.

사용자 지정 base URL은 다음 provider에서 지원됩니다.

- OpenAI
- Anthropic
- Gemini
- Groq
- Cohere
- DeepSeek
- xAI
- OpenRouter

<a name="provider-support"></a>
### Provider 지원

AI SDK는 다양한 기능에 대해 여러 provider를 지원합니다. 다음 표는 각 기능에서 사용할 수 있는 provider를 요약한 것입니다.

| Feature | Providers |
|---|---|
| Text | OpenAI, Anthropic, Gemini, Azure, Groq, xAI, DeepSeek, Mistral, Ollama |
| Images | OpenAI, Gemini, xAI |
| TTS | OpenAI, ElevenLabs |
| STT | OpenAI, ElevenLabs, Mistral |
| Embeddings | OpenAI, Gemini, Azure, Cohere, Mistral, Jina, VoyageAI |
| Reranking | Cohere, Jina |
| Files | OpenAI, Anthropic, Gemini |

코드에서 provider를 문자열 대신 `Laravel\Ai\Enums\Lab` enum을 사용하여 참조할 수 있습니다.

```php
use Laravel\Ai\Enums\Lab;

Lab::Anthropic;
Lab::OpenAI;
Lab::Gemini;
// ...
```

<a name="agents"></a>
## Agents

Agent는 Laravel AI SDK에서 AI provider와 상호작용하기 위한 기본 구성 요소입니다.  

각 agent는 다음을 캡슐화하는 전용 PHP 클래스입니다.

- 모델에게 전달할 지침(instructions)
- 대화 컨텍스트
- 사용 가능한 tools
- 출력 스키마

Agent는 특정 목적을 가진 전문 assistant라고 생각하면 이해하기 쉽습니다. 예를 들어 다음과 같은 역할을 할 수 있습니다.

- 영업 코치
- 문서 분석기
- 고객 지원 봇

Agent는 한 번 설정해 두면 애플리케이션 전반에서 반복적으로 사용할 수 있습니다.

다음 Artisan 명령어로 agent를 생성할 수 있습니다.

```shell
php artisan make:agent SalesCoach

php artisan make:agent SalesCoach --structured
```

생성된 agent 클래스에서는 다음 요소를 정의할 수 있습니다.

- 시스템 프롬프트 / instructions
- 메시지 컨텍스트
- 사용 가능한 tools
- 출력 스키마 (필요한 경우)

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
### 프롬프트

Agent를 사용하려면 먼저 인스턴스를 생성한 후 `prompt` 메서드를 호출합니다.

```php
$response = (new SalesCoach)
    ->prompt('Analyze this sales transcript...');

$response = SalesCoach::make()
    ->prompt('Analyze this sales transcript...');

return (string) $response;
```

`make` 메서드는 서비스 컨테이너를 통해 agent를 생성하므로 자동 의존성 주입을 사용할 수 있습니다.

생성자 인수도 전달할 수 있습니다.

```php
$agent = SalesCoach::make(user: $user);
```

또한 `prompt` 메서드에 추가 인수를 전달하여 기본 provider, 모델, HTTP timeout을 재정의할 수 있습니다.

```php
$response = (new SalesCoach)->prompt(
    'Analyze this sales transcript...',
    provider: Lab::Anthropic,
    model: 'claude-haiku-4-5-20251001',
    timeout: 120,
);
```

<a name="conversation-context"></a>
### 대화 컨텍스트

Agent가 `Conversational` 인터페이스를 구현하면 `messages` 메서드를 사용하여 이전 대화 컨텍스트를 반환할 수 있습니다.

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
#### 대화 기억하기

> **Note:** `RemembersConversations` trait를 사용하기 전에 `vendor:publish` Artisan 명령어로 AI SDK migration을 퍼블리시하고 실행해야 합니다. 이 migration은 대화를 저장하는 데 필요한 데이터베이스 테이블을 생성합니다.

Laravel이 agent의 대화 기록을 자동으로 저장하고 불러오도록 하려면 `RemembersConversations` trait를 사용할 수 있습니다.

이 trait는 `Conversational` 인터페이스를 직접 구현하지 않아도 데이터베이스에 대화 메시지를 저장하는 간단한 방법을 제공합니다.

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

사용자의 새로운 대화를 시작하려면 `prompt` 호출 전에 `forUser` 메서드를 호출합니다.

```php
$response = (new SalesCoach)->forUser($user)->prompt('Hello!');

$conversationId = $response->conversationId;
```

응답에는 `conversationId`가 포함되며 이후 참조를 위해 저장할 수 있습니다. 또한 `agent_conversations` 테이블에서 사용자의 모든 대화를 조회할 수도 있습니다.

기존 대화를 계속하려면 `continue` 메서드를 사용합니다.

```php
$response = (new SalesCoach)
    ->continue($conversationId, as: $user)
    ->prompt('Tell me more about that.');
```

`RemembersConversations` trait를 사용하면 이전 메시지가 자동으로 로드되어 대화 컨텍스트에 포함됩니다. 또한 각 상호작용 이후 사용자 메시지와 assistant 메시지가 자동으로 데이터베이스에 저장됩니다.