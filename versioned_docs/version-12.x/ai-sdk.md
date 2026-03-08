# Laravel AI SDK

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [사용자 지정 Base URL](#custom-base-urls)
    - [Provider 지원](#provider-support)
- [Agents](#agents)
    - [프롬프트 작성](#prompting)
    - [대화 컨텍스트](#conversation-context)
    - [구조화된 출력](#structured-output)
    - [첨부 파일](#attachments)
    - [스트리밍](#streaming)
    - [브로드캐스팅](#broadcasting)
    - [큐 처리](#queueing)
    - [도구](#tools)
    - [Provider 도구](#provider-tools)
    - [미들웨어](#middleware)
    - [익명 Agents](#anonymous-agents)
    - [Agent 설정](#agent-configuration)
- [이미지](#images)
- [오디오 (TTS)](#audio)
- [전사 (STT)](#transcription)
- [임베딩](#embeddings)
    - [임베딩 조회](#querying-embeddings)
    - [임베딩 캐싱](#caching-embeddings)
- [재정렬 (Reranking)](#reranking)
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
    - [재정렬](#testing-reranking)
    - [파일](#testing-files)
    - [벡터 스토어](#testing-vector-stores)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel AI SDK](https://github.com/laravel/ai)는 OpenAI, Anthropic, Gemini 등 다양한 AI provider와 상호작용할 수 있도록 통합되고 표현력이 높은 API를 제공합니다.  
AI SDK를 사용하면 도구와 구조화된 출력을 갖춘 지능형 에이전트를 구축하고, 이미지를 생성하며, 오디오를 합성하거나 전사하고, 벡터 임베딩을 생성하는 등 다양한 작업을 **일관된 Laravel 친화적인 인터페이스**로 수행할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

Composer를 통해 Laravel AI SDK를 설치할 수 있습니다:

```shell
composer require laravel/ai
```

다음으로 `vendor:publish` Artisan 명령어를 사용하여 AI SDK의 설정 및 마이그레이션 파일을 게시해야 합니다:

```shell
php artisan vendor:publish --provider="Laravel\Ai\AiServiceProvider"
```

마지막으로 애플리케이션의 데이터베이스 마이그레이션을 실행합니다. 이 작업을 통해 AI SDK가 대화 기록을 저장하는 데 사용하는 `agent_conversations` 및 `agent_conversation_messages` 테이블이 생성됩니다:

```shell
php artisan migrate
```

<a name="configuration"></a>
### 설정

AI provider의 인증 정보는 애플리케이션의 `config/ai.php` 설정 파일 또는 `.env` 파일에 환경 변수로 정의할 수 있습니다:

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

텍스트, 이미지, 오디오, 전사, 임베딩에 사용되는 기본 모델 역시 `config/ai.php` 설정 파일에서 지정할 수 있습니다.

<a name="custom-base-urls"></a>
### 사용자 지정 Base URL

기본적으로 Laravel AI SDK는 각 provider의 공개 API 엔드포인트에 직접 연결합니다.  
하지만 프록시 서비스를 통해 요청을 라우팅해야 하는 경우가 있을 수 있습니다. 예를 들어 API 키 관리 중앙화, 요청 속도 제한(rate limiting), 또는 기업 내부 게이트웨이를 통한 트래픽 라우팅 등이 있습니다.

이 경우 provider 설정에 `url` 파라미터를 추가하여 사용자 지정 Base URL을 설정할 수 있습니다:

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

이 기능은 LiteLLM이나 Azure OpenAI Gateway 같은 프록시 서비스를 통해 요청을 라우팅할 때 유용합니다.

다음 provider는 사용자 지정 Base URL을 지원합니다:

OpenAI, Anthropic, Gemini, Groq, Cohere, DeepSeek, xAI, OpenRouter

<a name="provider-support"></a>
### Provider 지원

AI SDK는 다양한 기능에서 여러 provider를 지원합니다. 다음 표는 기능별 지원 provider를 정리한 것입니다:

| Feature | Providers |
|---|---|
| Text | OpenAI, Anthropic, Gemini, Azure, Groq, xAI, DeepSeek, Mistral, Ollama |
| Images | OpenAI, Gemini, xAI |
| TTS | OpenAI, ElevenLabs |
| STT | OpenAI, ElevenLabs, Mistral |
| Embeddings | OpenAI, Gemini, Azure, Cohere, Mistral, Jina, VoyageAI |
| Reranking | Cohere, Jina |
| Files | OpenAI, Anthropic, Gemini |

코드에서 provider를 문자열 대신 `Laravel\Ai\Enums\Lab` enum을 사용해 참조할 수 있습니다:

```php
use Laravel\Ai\Enums\Lab;

Lab::Anthropic;
Lab::OpenAI;
Lab::Gemini;
// ...
```

<a name="agents"></a>
## Agents

Agents는 Laravel AI SDK에서 AI provider와 상호작용하기 위한 **핵심 구성 요소**입니다.  
각 agent는 하나의 PHP 클래스이며, 대형 언어 모델과 상호작용하기 위해 필요한 다음 요소를 포함합니다:

- 지침 (instructions)
- 대화 컨텍스트
- 사용 가능한 도구
- 출력 스키마

즉, agent는 특정 목적을 가진 **전문 어시스턴트**라고 생각할 수 있습니다. 예를 들어:

- 세일즈 코치
- 문서 분석기
- 고객 지원 봇

Agent는 `make:agent` Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:agent SalesCoach

php artisan make:agent SalesCoach --structured
```

생성된 agent 클래스에서는 시스템 프롬프트(지침), 메시지 컨텍스트, 사용 가능한 도구, 출력 스키마 등을 정의할 수 있습니다:

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

(문서의 길이 제한으로 인해 이후 섹션 번역은 다음 메시지에서 계속됩니다.)