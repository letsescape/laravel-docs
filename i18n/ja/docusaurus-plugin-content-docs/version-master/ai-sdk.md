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
    - [Provider Tools](#provider-tools)
    - [Middleware](#middleware)
    - [Anonymous Agents](#anonymous-agents)
    - [Agent Configuration](#agent-configuration)
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
[Laravel AI SDK](https://github.com/laravel/ai) は、OpenAI、Anthropic、Gemini などの AI プロバイダと対話するための統合された表現力豊かな API を提供します。 AI SDK を使用すると、一貫した Laravel フレンドリーなインターフェイスを使用して、ツールと構造化された出力を備えたインテリジェント エージェントの構築、画像の生成、音声の合成と転写、ベクトル埋め込みの作成などを行うことができます。

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- You can install the Laravel AI SDK via Composer: -->
Laravel AI SDK は Composer 経由でインストールできます。

```shell
composer require laravel/ai
```

<!-- Next, you should publish the AI SDK configuration and migration files using the `vendor:publish` Artisan command: -->
次に、`vendor:publish` Artisan コマンドを使用して、AI SDK 構成ファイルと移行ファイルを公開する必要があります。

```shell
php artisan vendor:publish --provider="Laravel\Ai\AiServiceProvider"
```

<!-- Finally, you should run your application's database migrations. This will create a `agent_conversations` and `agent_conversation_messages` table that the AI SDK uses to power its conversation storage: -->
最後に、アプリケーションのデータベース移行を実行する必要があります。これにより、AI SDK が会話ストレージを強化するために使用する `agent_conversations` テーブルと `agent_conversation_messages` テーブルが作成されます。

```shell
php artisan migrate
```

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- You may define your AI provider credentials in your application's `config/ai.php` configuration file or as environment variables in your application's `.env` file: -->
AI プロバイダの資格情報は、アプリケーションの `config/ai.php` 構成ファイルで定義することも、アプリケーションの `.env` ファイルで環境変数として定義することもできます。

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

<!-- The default models used for text, images, audio, transcription, and embeddings may also be configured in your application's `config/ai.php` configuration file. -->
テキスト、画像、オーディオ、文字起こし、埋め込みに使用されるデフォルトのモデルは、アプリケーションの `config/ai.php` 構成ファイルで構成することもできます。

<a name="custom-base-urls"></a>
<!-- ### Custom Base URLs -->
### Custom Base URLs

<!-- By default, the Laravel AI SDK connects directly to each provider's public API endpoint. However, you may need to route requests through a different endpoint - for example, when using a proxy service to centralize API key management, implement rate limiting, or route traffic through a corporate gateway. -->
デフォルトでは、Laravel AI SDK は各プロバイダのパブリック API エンドポイントに直接接続します。ただし、プロキシ サービスを使用して API キー管理を一元化したり、レート制限を実装したり、企業ゲートウェイ経由でトラフィックをルーティングしたりする場合など、別のエンドポイントを介してリクエストをルーティングする必要がある場合があります。

<!-- You may configure custom base URLs by adding a `url` parameter to your provider configuration: -->
プロバイダ設定に `url` パラメータを追加することで、カスタム ベース URL を設定できます。

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

<!-- This is useful when routing requests through a proxy service (such as LiteLLM or Azure OpenAI Gateway) or using alternative endpoints. -->
これは、プロキシ サービス (LiteLLM や Azure OpenAI Gateway など) を介して要求をルーティングする場合、または代替エンドポイントを使用する場合に便利です。

<!-- Custom base URLs are supported for the following providers: OpenAI, Anthropic, Gemini, Groq, Cohere, DeepSeek, xAI, and OpenRouter. -->
カスタム ベース URL は、OpenAI、Anthropic、Gemini、Groq、Cohere、DeepSeek、xAI、OpenRouter のプロバイダでサポートされています。

<a name="provider-support"></a>
<!-- ### Provider Support -->
### Provider Support

<!-- The AI SDK supports a variety of providers across its features. The following table summarizes which providers are available for each feature: -->
AI SDK は、その機能全体にわたってさまざまなプロバイダをサポートします。次の表は、各機能で利用できるプロバイダをまとめたものです。

| 特徴 | プロバイダ |
|---|---|
| 文章 | OpenAI、Anthropic、Gemini、Azure、Groq、xAI、DeepSeek、Mistral、Ollama |
| 画像 | OpenAI、Gemini、xAI |
| TTS | OpenAI、ElevenLabs |
| STT | OpenAI、ElevenLabs、Mistral |
| 埋め込み | OpenAI、Gemini、Azure、Cohere、Mistral、Jina、VoyageAI |
| 再ランキング | Cohere、Jina |
| ファイル | OpenAI、Anthropic、Gemini |

<!-- The `Laravel\Ai\Enums\Lab` enum may be used to reference providers throughout your code instead of using plain strings: -->
`Laravel\Ai\Enums\Lab` 列挙型は、プレーン文字列を使用する代わりに、コード全体でプロバイダを参照するために使用できます。

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
エージェントは、Laravel AI SDK で AI プロバイダと対話するための基本的な構成要素です。各エージェントは、大規模な言語モデルと対話するために必要な命令、会話コンテキスト、ツール、出力スキーマをカプセル化する専用の PHP クラスです。エージェントは、一度構成すれば、アプリケーション全体で必要に応じてプロンプトを表示できる、セールス コーチ、ドキュメント アナライザー、サポート ボットなどの専門アシスタントと考えてください。

<!-- You can create an agent via the `make:agent` Artisan command: -->
`make:agent` Artisan コマンドを使用してエージェントを作成できます。

```shell
php artisan make:agent SalesCoach

php artisan make:agent SalesCoach --structured
```

<!-- Within the generated agent class, you can define the system prompt / instructions, message context, available tools, and output schema (if applicable): -->
生成されたエージェント クラス内で、システム プロンプト/指示、メッセージ コンテキスト、利用可能なツール、および出力スキーマ (該当する場合) を定義できます。

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
エージェントにプロンプ​​トを表示するには、まず `make` メソッドまたは標準のインスタンス化を使用してインスタンスを作成し、次に `prompt` を呼び出します。

```php
$response = (new SalesCoach)
    ->prompt('Analyze this sales transcript...');

$response = SalesCoach::make()
    ->prompt('Analyze this sales transcript...');

return (string) $response;
```

<!-- The `make` method resolves your agent from the container, allowing automatic dependency injection. You may also pass arguments to the agent's constructor: -->
`make` メソッドはコンテナからエージェントを解決し、自動依存注入を可能にします。エージェントのコンストラクターに引数を渡すこともできます。

```php
$agent = SalesCoach::make(user: $user);
```

<!-- By passing additional arguments to the `prompt` method, you may override the default provider, model, or HTTP timeout when prompting: -->
追加の引数を `prompt` メソッドに渡すことで、プロンプトが表示されたときにデフォルトのプロバイダ、モデル、または HTTP タイムアウトをオーバーライドできます。

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
エージェントが `Conversational` インターフェイスを実装している場合、該当する場合は、`messages` メソッドを使用して前の会話コンテキストを返すことができます。

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

> **注意:** `RemembersConversations` トレイトを使用する前に、`vendor:publish` Artisan コマンドを使用して AI SDK 移行を公開し、実行する必要があります。これらの移行により、会話を保存するために必要なデータベース テーブルが作成されます。

<!-- If you would like Laravel to automatically store and retrieve conversation history for your agent, you may use the `RemembersConversations` trait. This trait provides a simple way to persist conversation messages to the database without manually implementing the `Conversational` interface: -->
Laravel にエージェントの会話履歴を自動的に保存および取得させたい場合は、`RemembersConversations` トレイトを使用できます。この特性は、`Conversational` インターフェイスを手動で実装せずに、データベースに会話メッセージを永続化する簡単な方法を提供します。

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

<!-- To start a new conversation for a user, call the `forUser` method before prompting: -->
ユーザーに対して新しい会話を開始するには、プロンプトを表示する前に `forUser` メソッドを呼び出します。

```php
$response = (new SalesCoach)->forUser($user)->prompt('Hello!');

$conversationId = $response->conversationId;
```

<!-- The conversation ID is returned on the response and can be stored for future reference, or you can retrieve all of a user's conversations from the `agent_conversations` table directly. -->
会話 ID は応答で返され、将来の参照のために保存したり、`agent_conversations` テーブルからユーザーのすべての会話を直接取得したりできます。

<!-- To continue an existing conversation, use the `continue` method: -->
既存の会話を続行するには、`continue` メソッドを使用します。

```php
$response = (new SalesCoach)
    ->continue($conversationId, as: $user)
    ->prompt('Tell me more about that.');
```

<!-- When using the `RemembersConversations` trait, previous messages are automatically loaded and included in the conversation context when prompting. New messages (both user and assistant) are automatically stored after each interaction. -->
`RemembersConversations` トレイトを使用すると、以前のメッセージが自動的にロードされ、プロンプトが表示されたときに会話コンテキストに組み込まれます。新しいメッセージ (ユーザーとアシスタントの両方) は、各対話後に自動的に保存されます。

<a name="structured-output"></a>
<!-- ### Structured Output -->
### Structured Output

<!-- If you would like your agent to return structured output, implement the `HasStructuredOutput` interface, which requires that your agent define a `schema` method: -->
エージェントが構造化された出力を返すようにするには、`HasStructuredOutput` インターフェイスを実装します。これには、エージェントが `schema` メソッドを定義する必要があります。

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
構造化された出力を返すエージェントにプロンプ​​トを表示する場合、配列のように返された `StructuredAgentResponse` にアクセスできます。

```php
$response = (new SalesCoach)->prompt('Analyze this sales transcript...');

return $response['score'];
```

<a name="attachments"></a>
<!-- ### Attachments -->
### Attachments

<!-- When prompting, you may also pass attachments with the prompt to allow the model to inspect images and documents: -->
プロンプトを表示するときに、プロンプトとともに添付ファイルを渡して、モデルが画像やドキュメントを検査できるようにすることもできます。

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
同様に、`Laravel\Ai\Files\Image` クラスを使用して、プロンプトに画像を添付できます。

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
`stream` メソッドを呼び出すことで、エージェントの応答をストリーミングできます。返される `StreamableAgentResponse` は、ストリーミング応答 (SSE) をクライアントに自動的に送信するルートから返される場合があります。

```php
use App\Ai\Agents\SalesCoach;

Route::get('/coach', function () {
    return (new SalesCoach)->stream('Analyze this sales transcript...');
});
```

<!-- The `then` method may be used to provide a closure that will be invoked when the entire response has been streamed to the client: -->
`then` メソッドは、応答全体がクライアントにストリーミングされたときに呼び出されるクロージャを提供するために使用できます。

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
あるいは、ストリーミングされたイベントを手動で反復処理することもできます。

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
ストリーミング可能な応答で `usingVercelDataProtocol` メソッドを呼び出すことにより、[Vercel AI SDK stream protocol](https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocol) を使用してイベントをストリーミングできます。

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
ストリーミング イベントは、いくつかの異なる方法でブロードキャストできます。まず、ストリーミング イベントで `broadcast` メソッドまたは `broadcastNow` メソッドを呼び出すだけです。

```php
use App\Ai\Agents\SalesCoach;
use Illuminate\Broadcasting\Channel;

$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

foreach ($stream as $event) {
    $event->broadcast(new Channel('channel-name'));
}
```

<!-- Or, you can invoke an agent's `broadcastOnQueue` method to queue the agent operation and broadcast the streamed events as they are available: -->
または、エージェントの `broadcastOnQueue` メソッドを呼び出して、エージェントの操作をキューに入れ、ストリーミング イベントが利用可能になったときにブロードキャストすることもできます。

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
エージェントの `queue` メソッドを使用すると、エージェントにプロンプ​​トを表示しながら、エージェントがバックグラウンドで応答を処理できるようにすることで、アプリケーションの高速性と応答性を維持できます。 `then` メソッドと `catch` メソッドは、応答が利用可能な場合、または例外が発生した場合に呼び出されるクロージャを登録するために使用できます。

```php
use Illuminate\Http\Request;
use Laravel\Ai\Responses\AgentResponse;
use Throwable;

Route::post('/coach', function (Request $request) {
    return (new SalesCoach)
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
ツールを使用して、エージェントがプロンプトに応答する際に利用できる追加機能を提供できます。ツールは、`make:tool` Artisan コマンドを使用して作成できます。

```shell
php artisan make:tool RandomNumberGenerator
```

<!-- The generated tool will be placed in your application's `app/Ai/Tools` directory. Each tool contains a `handle` method that will be invoked by the agent when it needs to utilize the tool: -->
生成されたツールは、アプリケーションの `app/Ai/Tools` ディレクトリに配置されます。各ツールには、ツールを利用する必要があるときにエージェントによって呼び出される `handle` メソッドが含まれています。

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
ツールを定義したら、エージェントの `tools` メソッドからツールを返すことができます。

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
`SimilaritySearch` ツールを使用すると、エージェントはデータベースに保存されているベクトル埋め込みを使用して、特定のクエリに類似したドキュメントを検索できます。これは、アプリケーションのデータを検索するためのアクセス権をエージェントに付与する場合の検索拡張生成 (RAG) に役立ちます。

<!-- The simplest way to create a similarity search tool is using the `usingModel` method with an Eloquent model that has vector embeddings: -->
類似性検索ツールを作成する最も簡単な方法は、ベクトル埋め込みを含む Eloquent モデルで `usingModel` メソッドを使用することです。

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
最初の引数は Eloquent モデル クラスで、2 番目の引数はベクトル エンベディングを含む列です。

<!-- You may also provide a minimum similarity threshold between `0.0` and `1.0` and a closure to customize the query: -->
`0.0` と `1.0` の間の最小類似性しきい値とクロージャを指定して、クエリをカスタマイズすることもできます。

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
さらに制御するには、検索結果を返すカスタム クロージャを含む類似性検索ツールを作成できます。

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
`withDescription` メソッドを使用してツールの説明をカスタマイズできます。

```php
SimilaritySearch::usingModel(Document::class, 'embedding')
    ->withDescription('Search the knowledge base for relevant articles.'),
```

<a name="provider-tools"></a>
<!-- ### Provider Tools -->
### Provider Tools

<!-- Provider tools are special tools implemented natively by AI providers, offering capabilities like web searching, URL fetching, and file searching. Unlike regular tools, provider tools are executed by the provider itself rather than your application. -->
プロバイダ ツールは、AI プロバイダによってネイティブに実装される特別なツールで、Web 検索、URL フェッチ、ファイル検索などの機能を提供します。通常のツールとは異なり、プロバイダ ツールはアプリケーションではなくプロバイダ自体によって実行されます。

<!-- Provider tools can be returned by your agent's `tools` method. -->
プロバイダ ツールは、エージェントの `tools` メソッドによって返されます。

<a name="web-search"></a>
<!-- #### Web Search -->
#### Web Search

<!-- The `WebSearch` provider tool allows agents to search the web for real-time information. This is useful for answering questions about current events, recent data, or topics that may have changed since the model's training cutoff. -->
`WebSearch` プロバイダ ツールを使用すると、エージェントは Web でリアルタイム情報を検索できます。これは、現在のイベント、最近のデータ、またはモデルのトレーニングのカットオフ以降に変更された可能性のあるトピックに関する質問に答えるのに役立ちます。

<!-- **Supported Providers:** Anthropic, OpenAI, Gemini -->
**サポートされているプロバイダ:** Anthropic、OpenAI、Gemini

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
Web 検索ツールを構成して、検索数を制限したり、結果を特定のドメインに制限したりすることができます。

```php
(new WebSearch)->max(5)->allow(['laravel.com', 'php.net']),
```

<!-- To refine search results based on user location, use the `location` method: -->
ユーザーの場所に基づいて検索結果を絞り込むには、`location` メソッドを使用します。

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
`WebFetch` プロバイダ ツールを使用すると、エージェントは Web ページのコンテンツをフェッチして読み取ることができます。これは、エージェントが特定の URL を分析したり、既知の Web ページから詳細情報を取得したりする必要がある場合に役立ちます。

<!-- **Supported providers:** Anthropic, Gemini -->
**サポートされているプロバイダ:** Anthropic、Gemini

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
Web 取得ツールを設定して、取得数を制限したり、特定のドメインに制限したりすることができます。

```php
(new WebFetch)->max(3)->allow(['docs.laravel.com']),
```

<a name="file-search"></a>
<!-- #### File Search -->
#### File Search

<!-- The `FileSearch` provider tool allows agents to search through [files](#files) stored in [vector stores](#vector-stores). This enables retrieval-augmented generation (RAG) by allowing the agent to search your uploaded documents for relevant information. -->
`FileSearch` プロバイダ ツールを使用すると、エージェントは [files](#files)（[vector stores](#vector-stores) に保存されているもの）を検索できます。これにより、エージェントがアップロードされたドキュメントで関連情報を検索できるようになり、検索拡張生成 (RAG) が可能になります。

<!-- **Supported providers:** OpenAI, Gemini -->
**サポートされているプロバイダ:** OpenAI、Gemini

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
複数のベクトル ストア ID を指定して、複数のストアを検索できます。

```php
new FileSearch(stores: ['store_1', 'store_2']);
```

<!-- If your files have [metadata](#adding-files-to-stores), you may filter the search results by providing a `where` argument. For simple equality filters, pass an array: -->
ファイルに [metadata](#adding-files-to-stores) がある場合は、`where` 引数を指定して検索結果をフィルタリングできます。単純な等価フィルターの場合は、配列を渡します。

```php
new FileSearch(stores: ['store_id'], where: [
    'author' => 'Taylor Otwell',
    'year' => 2026,
]);
```

<!-- For more complex filters, you may pass a closure that receives a `FileSearchQuery` instance: -->
より複雑なフィルターの場合は、`FileSearchQuery` インスタンスを受け取るクロージャーを渡すことができます。

```php
use Laravel\Ai\Providers\Tools\FileSearchQuery;

new FileSearch(stores: ['store_id'], where: fn (FileSearchQuery $query) =>
    $query->where('author', 'Taylor Otwell')
        ->whereNot('status', 'draft')
        ->whereIn('category', ['news', 'updates'])
);
```

<a name="middleware"></a>
<!-- ### Middleware -->
### Middleware

<!-- Agents support middleware, allowing you to intercept and modify prompts before they are sent to the provider. Middleware can be created using the `make:agent-middleware` Artisan command: -->
エージェントはミドルウェアをサポートしているため、プロンプトがプロバイダに送信される前にインターセプトして変更することができます。ミドルウェアは、`make:agent-middleware` Artisan コマンドを使用して作成できます。

```shell
php artisan make:agent-middleware LogPrompts
```

<!-- The generated middleware will be placed in your application's `app/Ai/Middleware` directory. To add middleware to an agent, implement the `HasMiddleware` interface and define a `middleware` method that returns an array of middleware classes: -->
生成されたミドルウェアは、アプリケーションの `app/Ai/Middleware` ディレクトリに配置されます。エージェントにミドルウェアを追加するには、`HasMiddleware` インターフェイスを実装し、ミドルウェア クラスの配列を返す `middleware` メソッドを定義します。

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
各ミドルウェア クラスは、`AgentPrompt` と `Closure` を受け取り、プロンプトを次のミドルウェアに渡す `handle` メソッドを定義する必要があります。

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
エージェントの処理が完了した後に、応答で `then` メソッドを使用してコードを実行できます。これは、同期応答とストリーミング応答の両方で機能します。

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
場合によっては、専用のエージェント クラスを作成せずにモデルをすばやく操作したい場合があります。 `agent` 関数を使用して、アドホックな匿名エージェントを作成できます。

```php
use function Laravel\Ai\{agent};

$response = agent(
    instructions: 'You are an expert at software development.',
    messages: [],
    tools: [],
)->prompt('Tell me about Laravel')
```

<!-- Anonymous agents may also produce structured output: -->
匿名エージェントは構造化された出力を生成することもあります。

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
PHP 属性を使用して、エージェントのテキスト生成オプションを構成できます。次の属性が使用可能です。

<!--
- `MaxSteps`: The maximum number of steps the agent may take when using tools.
- `MaxTokens`: The maximum number of tokens the model may generate.
- `Model`: The model the agent should use.
- `Provider`: The AI provider (or providers for failover) to use for the agent.
- `Temperature`: The sampling temperature to use for generation (0.0 to 1.0).
- `Timeout`: The HTTP timeout in seconds for agent requests (default: 60).
- `UseCheapestModel`: Use the provider's cheapest text model for cost optimization.
- `UseSmartestModel`: Use the provider's most capable text model for complex tasks.
-->
- `MaxSteps`: ツールを使用するときにエージェントが実行できる最大ステップ数。
- `MaxTokens`: モデルが生成できるトークンの最大数。
- `Model`: エージェントが使用するモデル。
- `Provider`: エージェントに使用する AI プロバイダ (またはフェイルオーバー用のプロバイダ)。
- `Temperature`: 生成に使用するサンプリング温度 (0.0 ～ 1.0)。
- `Timeout`: エージェント要求の HTTP タイムアウト (秒単位) (デフォルト: 60)。
- `UseCheapestModel`: コストを最適化するために、プロバイダの最も安価なテキスト モデルを使用します。
- `UseSmartestModel`: 複雑なタスクにはプロバイダの最も機能的なテキスト モデルを使用します。

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Attributes\MaxSteps;
use Laravel\Ai\Attributes\MaxTokens;
use Laravel\Ai\Attributes\Model;
use Laravel\Ai\Attributes\Provider;
use Laravel\Ai\Attributes\Temperature;
use Laravel\Ai\Attributes\Timeout;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Promptable;

#[Provider(Lab::Anthropic)]
#[Model('claude-haiku-4-5-20251001')]
#[MaxSteps(10)]
#[MaxTokens(4096)]
#[Temperature(0.7)]
#[Timeout(120)]
class SalesCoach implements Agent
{
    use Promptable;

    // ...
}
```

<!-- The `UseCheapestModel` and `UseSmartestModel` attributes allow you to automatically select the most cost-effective or most capable model for a given provider without specifying a model name. This is useful when you want to optimize for cost or capability across different providers: -->
`UseCheapestModel` 属性と `UseSmartestModel` 属性を使用すると、モデル名を指定せずに、特定のプロバイダに対して最もコスト効率の高いモデルまたは最も機能的なモデルを自動的に選択できます。これは、さまざまなプロバイダ間でコストや機能を最適化する場合に役立ちます。

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

<a name="images"></a>
<!-- ## Images -->
## Images

<!-- The `Laravel\Ai\Image` class may be used to generate images using the `openai`, `gemini`, or `xai` providers: -->
`Laravel\Ai\Image` クラスは、`openai`、`gemini`、または `xai` プロバイダを使用してイメージを生成するために使用できます。

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')->generate();

$rawContent = (string) $image;
```

<!-- The `square`, `portrait`, and `landscape` methods may be used to control the aspect ratio of the image, while the `quality` method may be used to guide the model on final image quality (`high`, `medium`, `low`). The `timeout` method may be used to specify the HTTP timeout in seconds: -->
`square`、`portrait`、および `landscape` メソッドは画像のアスペクト比を制御するために使用できますが、`quality` メソッドは最終的な画像品質 (`high`、`medium`、`low`) についてモデルをガイドするために使用できます。 `timeout` メソッドを使用して、HTTP タイムアウトを秒単位で指定できます。

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')
    ->quality('high')
    ->landscape()
    ->timeout(120)
    ->generate();
```

<!-- You may attach reference images using the `attachments` method: -->
`attachments` メソッドを使用して参照画像を添付できます。

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
生成されたイメージは、アプリケーションの `config/filesystems.php` 構成ファイルで構成されたデフォルトのディスクに簡単に保存できます。

```php
$image = Image::of('A donut sitting on the kitchen counter');

$path = $image->store();
$path = $image->storeAs('image.jpg');
$path = $image->storePublicly();
$path = $image->storePubliclyAs('image.jpg');
```

<!-- Image generation may also be queued: -->
イメージ生成もキューに入れられる場合があります。

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
`Laravel\Ai\Audio` クラスは、指定されたテキストから音声を生成するために使用できます。

```php
use Laravel\Ai\Audio;

$audio = Audio::of('I love coding with Laravel.')->generate();

$rawContent = (string) $audio;
```

<!-- The `male`, `female`, and `voice` methods may be used to determine the voice of the generated audio: -->
`male`、`female`、および `voice` メソッドを使用して、生成されるオーディオの音声を決定できます。

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->generate();

$audio = Audio::of('I love coding with Laravel.')
    ->voice('voice-id-or-name')
    ->generate();
```

<!-- Similarly, the `instructions` method may be used to dynamically coach the model on how the generated audio should sound: -->
同様に、`instructions` メソッドを使用して、生成されたオーディオがどのように聞こえるべきかについてモデルを動的に指導することができます。

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->instructions('Said like a pirate')
    ->generate();
```

<!-- Generated audio may be easily stored on the default disk configured in your application's `config/filesystems.php` configuration file: -->
生成されたオーディオは、アプリケーションの `config/filesystems.php` 構成ファイルで構成されたデフォルトのディスクに簡単に保存できます。

```php
$audio = Audio::of('I love coding with Laravel.')->generate();

$path = $audio->store();
$path = $audio->storeAs('audio.mp3');
$path = $audio->storePublicly();
$path = $audio->storePubliclyAs('audio.mp3');
```

<!-- Audio generation may also be queued: -->
オーディオ生成もキューに入れられる場合があります。

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
`Laravel\Ai\Transcription` クラスは、指定された音声のトランスクリプトを生成するために使用できます。

```php
use Laravel\Ai\Transcription;

$transcript = Transcription::fromPath('/home/laravel/audio.mp3')->generate();
$transcript = Transcription::fromStorage('audio.mp3')->generate();
$transcript = Transcription::fromUpload($request->file('audio'))->generate();

return (string) $transcript;
```

<!-- The `diarize` method may be used to indicate you would like the response to include the diarized transcript in addition to the raw text transcript, allowing you to access the segmented transcript by speaker: -->
`diarize` メソッドを使用すると、生のテキストのトランスクリプトに加えて話者分離されたトランスクリプトを応答に含めることを希望することを示すことができ、これにより、話者ごとにセグメント化されたトランスクリプトにアクセスできるようになります。

```php
$transcript = Transcription::fromStorage('audio.mp3')
    ->diarize()
    ->generate();
```

<!-- Transcription generation may also be queued: -->
文字起こしの生成もキューに入れられる場合があります。

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
Laravel の `Stringable` クラスから利用できる新しい `toEmbeddings` メソッドを使用すると、任意の文字列のベクトル埋め込みを簡単に生成できます。

```php
use Illuminate\Support\Str;

$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

<!-- Alternatively, you may use the `Embeddings` class to generate embeddings for multiple inputs at once: -->
あるいは、`Embeddings` クラスを使用して、複数の入力の埋め込みを一度に生成することもできます。

```php
use Laravel\Ai\Embeddings;

$response = Embeddings::for([
    'Napa Valley has great wine.',
    'Laravel is a PHP framework.',
])->generate();

$response->embeddings; // [[0.123, 0.456, ...], [0.789, 0.012, ...]]
```

<!-- You may specify the dimensions and provider for the embeddings: -->
埋め込みのディメンションとプロバイダを指定できます。

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->dimensions(1536)
    ->generate(Lab::OpenAI, 'text-embedding-3-small');
```

<a name="querying-embeddings"></a>
<!-- ### Querying Embeddings -->
### Querying Embeddings

<!-- Once you have generated embeddings, you will typically store them in a `vector` column in your database for later querying. Laravel provides native support for vector columns on PostgreSQL via the `pgvector` extension. To get started, define a `vector` column in your migration, specifying the number of dimensions: -->
埋め込みを生成したら、通常は、後でクエリできるようにデータベースの `vector` 列に格納します。 Laravel は、`pgvector` 拡張機能を介して PostgreSQL 上のベクター列のネイティブ サポートを提供します。まず、移行で `vector` 列を定義し、次元の数を指定します。

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
類似性検索を高速化するためにベクトル インデックスを追加することもできます。ベクトル列で `index` を呼び出すと、Laravel はコサイン距離を使用して HNSW インデックスを自動的に作成します。

```php
$table->vector('embedding', dimensions: 1536)->index();
```

<!-- On your Eloquent model, you should cast the vector column to an `array`: -->
Eloquent モデルでは、ベクトル列を `array` にcastする必要があります。

```php
protected function casts(): array
{
    return [
        'embedding' => 'array',
    ];
}
```

<!-- To query for similar records, use the `whereVectorSimilarTo` method. This method filters results by a minimum cosine similarity (between `0.0` and `1.0`, where `1.0` is identical) and orders the results by similarity: -->
同様のレコードをクエリするには、`whereVectorSimilarTo` メソッドを使用します。このメソッドは、最小のコサイン類似度 (`0.0` と `1.0` の間、`1.0` は同一) によって結果をフィルターし、類似度によって結果を並べ替えます。

```php
use App\Models\Document;

$documents = Document::query()
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

<!-- The `$queryEmbedding` may be an array of floats or a plain string. When a string is given, Laravel will automatically generate embeddings for it: -->
`$queryEmbedding` は、浮動小数点数の配列またはプレーン文字列の場合があります。文字列が指定されると、Laravel はその文字列の埋め込みを自動的に生成します。

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', 'best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

<!-- If you need more control, you may use the lower-level `whereVectorDistanceLessThan`, `selectVectorDistance`, and `orderByVectorDistance` methods independently: -->
より詳細な制御が必要な場合は、下位レベルの `whereVectorDistanceLessThan`、`selectVectorDistance`、および `orderByVectorDistance` メソッドを個別に使用できます。

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
エージェントにツールとして類似性検索を実行できるようにしたい場合は、[Similarity Search](#similarity-search) ツールのドキュメントを確認してください。

> [!NOTE]
> 現在、ベクター クエリは、`pgvector` 拡張機能を使用した PostgreSQL 接続でのみサポートされています。

<a name="caching-embeddings"></a>
<!-- ### Caching Embeddings -->
### Caching Embeddings

<!-- Embedding generation can be cached to avoid redundant API calls for identical inputs. To enable caching, set the `ai.caching.embeddings.cache` configuration option to `true`: -->
埋め込み生成をキャッシュして、同一の入力に対する冗長な API 呼び出しを回避できます。キャッシュを有効にするには、`ai.caching.embeddings.cache` 構成オプションを `true` に設定します。

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
キャッシュが有効になっている場合、埋め込みは 30 日間キャッシュされます。キャッシュ キーはプロバイダ、モデル、ディメンション、および入力コンテンツに基づいており、異なる構成で新しい埋め込みが生成される一方で、同一のリクエストがキャッシュされた結果を返すことが保証されます。

<!-- You may also enable caching for a specific request using the `cache` method, even when global caching is disabled: -->
グローバル キャッシュが無効になっている場合でも、`cache` メソッドを使用して特定のリクエストのキャッシュを有効にすることもできます。

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache()
    ->generate();
```

<!-- You may specify a custom cache duration in seconds: -->
カスタムのキャッシュ期間を秒単位で指定できます。

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache(seconds: 3600) // Cache for 1 hour
    ->generate();
```

<!-- The `toEmbeddings` Stringable method also accepts a `cache` argument: -->
`toEmbeddings` Stringable メソッドは、`cache` 引数も受け入れます。

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
再ランキングを使用すると、特定のクエリとの関連性に基づいてドキュメントのリストを並べ替えることができます。これは、意味的理解を使用して検索結果を改善するのに役立ちます。

<!-- The `Laravel\Ai\Reranking` class may be used to rerank documents: -->
`Laravel\Ai\Reranking` クラスは、ドキュメントを再ランク付けするために使用できます。

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
`limit` メソッドを使用して、返される結果の数を制限できます。

```php
$response = Reranking::of($documents)
    ->limit(5)
    ->rerank('search query');
```

<a name="reranking-collections"></a>
<!-- ### Reranking Collections -->
### Reranking Collections

<!-- For convenience, Laravel collections may be reranked using the `rerank` macro. The first argument specifies which field(s) to use for reranking, and the second argument is the query: -->
便宜上、Laravel コレクションは `rerank` マクロを使用して再ランク付けできます。最初の引数は再ランキングに使用するフィールドを指定し、2 番目の引数はクエリです。

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
結果の数を制限してプロバイダを指定することもできます。

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
`Laravel\Ai\Files` クラスまたは個々のファイル クラスは、後で会話で使用するために AI プロバイダでファイルを保存するために使用できます。これは、再アップロードせずに何度も参照したい大きなドキュメントやファイルの場合に便利です。

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
未加工のコンテンツやアップロードされたファイルを保存することもできます。

```php
use Laravel\Ai\Files;
use Laravel\Ai\Files\Document;

// Store raw content...
$stored = Document::fromString('Hello, World!', 'text/plain')->put();

// Store an uploaded file...
$stored = Document::fromUpload($request->file('document'))->put();
```

<!-- Once a file has been stored, you may reference the file when generating text via agents instead of re-uploading the file: -->
ファイルが保存されると、ファイルを再アップロードする代わりに、エージェント経由でテキストを生成するときにファイルを参照できます。

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
以前に保存されたファイルを取得するには、ファイル インスタンスで `get` メソッドを使用します。

```php
use Laravel\Ai\Files\Document;

$file = Document::fromId('file-id')->get();

$file->id;
$file->mimeType();
```

<!-- To delete a file from the provider, use the `delete` method: -->
プロバイダからファイルを削除するには、`delete` メソッドを使用します。

```php
Document::fromId('file-id')->delete();
```

<!-- By default, the `Files` class uses the default AI provider configured in your application's `config/ai.php` configuration file. For most operations, you may specify a different provider using the `provider` argument: -->
デフォルトでは、`Files` クラスは、アプリケーションの `config/ai.php` 構成ファイルで構成されたデフォルトの AI プロバイダを使用します。ほとんどの操作では、`provider` 引数を使用して別のプロバイダを指定できます。

```php
$response = Document::fromPath(
    '/home/laravel/document.pdf'
)->put(provider: Lab::Anthropic);
```

<a name="using-stored-files-in-conversations"></a>
<!-- ### Using Stored Files in Conversations -->
### Using Stored Files in Conversations

<!-- Once a file has been stored with a provider, you may reference it in agent conversations using the `fromId` method on the `Document` or `Image` classes: -->
ファイルがプロバイダに保存されたら、`Document` クラスまたは `Image` クラスの `fromId` メソッドを使用して、エージェントの会話でそのファイルを参照できます。

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
同様に、格納されたイメージは、`Image` クラスを使用して参照できます。

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
ベクター ストアを使用すると、検索拡張生成 (RAG) に使用できる、検索可能なファイルのコレクションを作成できます。 `Laravel\Ai\Stores` クラスは、ベクター ストアを作成、取得、削除するためのメソッドを提供します。

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
既存のベクター ストアを ID で取得するには、`get` メソッドを使用します。

```php
use Laravel\Ai\Stores;

$store = Stores::get('store_id');

$store->id;
$store->name;
$store->fileCounts;
$store->ready;
```

<!-- To delete a vector store, use the `delete` method on the `Stores` class or the store instance: -->
ベクター ストアを削除するには、`Stores` クラスまたはストア インスタンスで `delete` メソッドを使用します。

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
ベクター ストアを作成したら、`add` メソッドを使用してそれに [files](#files) を追加できます。ストアに追加されたファイルは、[file search provider tool](#file-search) を使用したセマンティック検索のために自動的にインデックス付けされます。

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

> **注意:** 通常、以前に保存されたファイルをベクター ストアに追加する場合、返されるドキュメント ID は、ファイルに以前に割り当てられた ID と一致します。ただし、一部のベクトル ストレージ プロバイダは、新しい異なる「ドキュメント ID」を返す場合があります。したがって、将来の参照のために両方の ID をデータベースに常に保存しておくことをお勧めします。

<!-- You may attach metadata to files when adding them to a store. This metadata can later be used to filter search results when using the [file search provider tool](#file-search): -->
ファイルをストアに追加するときに、ファイルにメタデータを添付できます。このメタデータは、後で [file search provider tool](#file-search) を使用するときに検索結果をフィルタリングするために使用できます。

```php
$store->add(Document::fromPath('/path/to/document.pdf'), metadata: [
    'author' => 'Taylor Otwell',
    'department' => 'Engineering',
    'year' => 2026,
]);
```

<!-- To remove a file from a store, use the `remove` method: -->
ストアからファイルを削除するには、`remove` メソッドを使用します。

```php
$store->remove('file_id');
```

<!-- Removing a file from a vector store does not remove it from the provider's [file storage](#files). To remove a file from the vector store and delete it permanently from file storage, use the `deleteFile` argument: -->
ベクター ストアからファイルを削除しても、プロバイダの [file storage](#files) からは削除されません。ファイルをベクター ストアから削除し、ファイルストレージから完全に削除するには、`deleteFile` 引数を使用します。

```php
$store->remove('file_abc123', deleteFile: true);
```

<a name="failover"></a>
<!-- ## Failover -->
## Failover

<!-- When prompting or generating other media, you may provide an array of providers / models to automatically failover to a backup provider / model if a service interruption or rate limit is encountered on the primary provider: -->
他のメディアをプロンプトまたは生成するときに、プライマリ プロバイダでサービスの中断またはレート制限が発生した場合に、バックアップ プロバイダ/モデルに自動的にフェイルオーバーするプロバイダ/モデルの配列を指定できます。

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Image;

$response = (new SalesCoach)->prompt(
    'Analyze this sales transcript...',
    provider: [Lab::OpenAI, Lab::Anthropic],
);

$image = Image::of('A donut sitting on the kitchen counter')
    ->generate(provider: [Lab::Gemini, Lab::xAI]);
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<a name="testing-agents"></a>
<!-- ### Agents -->
### Agents

<!-- To fake an agent's responses during tests, call the `fake` method on the agent class. You may optionally provide an array of responses or a closure: -->
テスト中にエージェントの応答を偽装するには、エージェント クラスで `fake` メソッドを呼び出します。必要に応じて、応答の配列またはクロージャを指定できます。

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

> **注意:** 構造化された出力を返すエージェント上で `Agent::fake()` が呼び出されると、Laravel はエージェントの定義された出力スキーマに一致する偽のデータを自動的に生成します。

<!-- After prompting the agent, you may make assertions about the prompts that were received: -->
エージェントにプロンプ​​トを出した後、受け取ったプロンプトについてアサーションを行うことができます。

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
キューに入れられたエージェント呼び出しの場合は、キューに入れられたアサーション メソッドを使用します。

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
すべてのエージェント呼び出しに対応する偽の応答があることを確認するには、`preventStrayPrompts` を使用できます。偽の応答が定義されていない状態でエージェントが呼び出された場合、例外がスローされます。

```php
SalesCoach::fake()->preventStrayPrompts();
```

<a name="testing-images"></a>
<!-- ### Images -->
### Images

<!-- Image generations may be faked by invoking the `fake` method on the `Image` class. Once image has been faked, various assertions may be performed against the recorded image generation prompts: -->
`Image` クラスの `fake` メソッドを呼び出すことで、イメージの生成を偽装することができます。画像が偽造されると、記録された画像生成プロンプトに対してさまざまなアサーションが実行される可能性があります。

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
イメージを生成した後、受信したプロンプトについてアサーションを行うことができます。

```php
Image::assertGenerated(function (ImagePrompt $prompt) {
    return $prompt->contains('sunset') && $prompt->isLandscape();
});

Image::assertNotGenerated('Missing prompt');

Image::assertNothingGenerated();
```

<!-- For queued image generations, use the queued assertion methods: -->
キューに入れられたイメージを生成するには、キューに入れられたアサーション メソッドを使用します。

```php
Image::assertQueued(
    fn (QueuedImagePrompt $prompt) => $prompt->contains('sunset')
);

Image::assertNotQueued('Missing prompt');

Image::assertNothingQueued();
```

<!-- To ensure all image generations have a corresponding fake response, you may use `preventStrayImages`. If an image is generated without a defined fake response, an exception will be thrown: -->
すべてのイメージ生成に対応する偽の応答があることを確認するには、`preventStrayImages` を使用できます。偽の応答が定義されていない状態でイメージが生成された場合、例外がスローされます。

```php
Image::fake()->preventStrayImages();
```

<a name="testing-audio"></a>
<!-- ### Audio -->
### Audio

<!-- Audio generations may be faked by invoking the `fake` method on the `Audio` class. Once audio has been faked, various assertions may be performed against the recorded audio generation prompts: -->
オーディオ生成は、`Audio` クラスの `fake` メソッドを呼び出すことによって偽装される可能性があります。オーディオが偽造されると、録音されたオーディオ生成プロンプトに対してさまざまなアサーションが実行される可能性があります。

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
音声を生成した後、受信したプロンプトについてアサーションを行うことができます。

```php
Audio::assertGenerated(function (AudioPrompt $prompt) {
    return $prompt->contains('Hello') && $prompt->isFemale();
});

Audio::assertNotGenerated('Missing prompt');

Audio::assertNothingGenerated();
```

<!-- For queued audio generations, use the queued assertion methods: -->
キューに入れられたオーディオ生成の場合は、キューに入れられたアサーション メソッドを使用します。

```php
Audio::assertQueued(
    fn (QueuedAudioPrompt $prompt) => $prompt->contains('Hello')
);

Audio::assertNotQueued('Missing prompt');

Audio::assertNothingQueued();
```

<!-- To ensure all audio generations have a corresponding fake response, you may use `preventStrayAudio`. If audio is generated without a defined fake response, an exception will be thrown: -->
すべてのオーディオ生成に対応する偽の応答があることを確認するには、`preventStrayAudio` を使用できます。定義された偽の応答なしでオーディオが生成された場合、例外がスローされます。

```php
Audio::fake()->preventStrayAudio();
```

<a name="testing-transcriptions"></a>
<!-- ### Transcriptions -->
### Transcriptions

<!-- Transcription generations may be faked by invoking the `fake` method on the `Transcription` class. Once transcription has been faked, various assertions may be performed against the recorded transcription generation prompts: -->
転写世代は、`Transcription` クラスの `fake` メソッドを呼び出すことによって偽装される可能性があります。転写が偽造されると、記録された転写生成プロンプトに対してさまざまなアサーションが実行される可能性があります。

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
文字起こしを生成した後、受信したプロンプトについてアサーションを行うことができます。

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
キューに入れられたトランスクリプション生成の場合は、キューに入れられたアサーション メソッドを使用します。

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
すべての転写生成に対応する偽の応答があることを確認するには、`preventStrayTranscriptions` を使用できます。偽の応答が定義されていない状態でトランスクリプションが生成された場合、例外がスローされます。

```php
Transcription::fake()->preventStrayTranscriptions();
```

<a name="testing-embeddings"></a>
<!-- ### Embeddings -->
### Embeddings

<!-- Embeddings generations may be faked by invoking the `fake` method on the `Embeddings` class. Once embeddings has been faked, various assertions may be performed against the recorded embeddings generation prompts: -->
埋め込みの生成は、`Embeddings` クラスの `fake` メソッドを呼び出すことによって偽装される可能性があります。エンベディングが偽造されると、記録されたエンベディング生成プロンプトに対してさまざまなアサーションが実行される可能性があります。

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
埋め込みを生成した後、受信したプロンプトについてアサーションを行うことができます。

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
キューに入れられた埋め込み生成の場合は、キューに入れられたアサーション メソッドを使用します。

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
すべての埋め込み生成に対応する偽の応答があることを確認するには、`preventStrayEmbeddings` を使用できます。偽の応答が定義されていない状態で埋め込みが生成された場合、例外がスローされます。

```php
Embeddings::fake()->preventStrayEmbeddings();
```

<a name="testing-reranking"></a>
<!-- ### Reranking -->
### Reranking

<!-- Reranking operations may be faked by invoking the `fake` method on the `Reranking` class: -->
再ランキング操作は、`Reranking` クラスの `fake` メソッドを呼び出すことで偽装される可能性があります。

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
再ランク付け後、実行された操作についてアサーションを行うことができます。

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
ファイル操作は、`Files` クラスの `fake` メソッドを呼び出すことで偽装される可能性があります。

```php
use Laravel\Ai\Files;

Files::fake();
```

<!-- Once file operations have been faked, you may make assertions about the uploads and deletions that occurred: -->
ファイル操作が偽装されると、発生したアップロードと削除についてアサーションを行うことができます。

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
ファイルの削除をアサートするには、ファイル ID を渡すことができます。

```php
Files::assertDeleted('file-id');
Files::assertNotDeleted('file-id');
Files::assertNothingDeleted();
```

<a name="testing-vector-stores"></a>
<!-- ### Vector Stores -->
### Vector Stores

<!-- Vector store operations may be faked by invoking the `fake` method on the `Stores` class. Faking stores will also fake [file operations](#files) automatically: -->
ベクター ストア操作は、`Stores` クラスの `fake` メソッドを呼び出すことで偽装される可能性があります。偽装ストアは自動的に [file operations](#files) も偽装します。

```php
use Laravel\Ai\Stores;

Stores::fake();
```

<!-- Once store operations have been faked, you may make assertions about the stores that were created or deleted: -->
ストア操作が偽装されると、作成または削除されたストアについてアサーションを行うことができます。

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
ストアの削除に対してアサートするには、ストア ID を指定できます。

```php
Stores::assertDeleted('store_id');
Stores::assertNotDeleted('other_store_id');
Stores::assertNothingDeleted();
```

<!-- To assert files were added or removed from a store, use the assertion methods on a given `Store` instance: -->
ファイルがストアに追加またはストアから削除されたことをアサートするには、特定の `Store` インスタンスでアサーション メソッドを使用します。

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
ファイルがプロバイダの [file storage](#files) に保存され、同じリクエスト内のベクター ストアに追加された場合、ファイルのプロバイダ ID がわからない可能性があります。この場合、クロージャを `assertAdded` メソッドに渡して、追加されたファイルのコンテンツに対してアサートできます。

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

<!-- The Laravel AI SDK dispatches a variety of [events](/docs/master/events), including: -->
Laravel AI SDK は、次のようなさまざまな [events](/docs/master/events) をディスパッチします。

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
これらのイベントのいずれかをリッスンして、AI SDK の使用情報を記録または保存できます。

