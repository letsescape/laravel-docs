# Laravel AI SDK (Laravel AI SDK)

- [Introduction](#introduction)
- [Installation](#installation)
    - [Configuration](#configuration)
    - [カスタムベースURL](#custom-base-urls)
    - [プロバイダのサポート](#provider-support)
- [Agents](#agents)
    - [Prompting](#prompting)
    - [会話のコンテキスト](#conversation-context)
    - [構造化された出力](#structured-output)
    - [Attachments](#attachments)
    - [Streaming](#streaming)
    - [Broadcasting](#broadcasting)
    - [Queueing](#queueing)
    - [Tools](#tools)
    - [プロバイダツール](#provider-tools)
    - [Middleware](#middleware)
    - [匿名エージェント](#anonymous-agents)
    - [エージェント構成](#agent-configuration)
- [Images](#images)
- [オーディオ (TTS)](#audio)
- [転写（STT）](#transcription)
- [Embeddings](#embeddings)
    - [埋め込みのクエリ](#querying-embeddings)
    - [埋め込みのキャッシュ](#caching-embeddings)
- [Reranking](#reranking)
- [Files](#files)
- [ベクターストア](#vector-stores)
    - [ストアにファイルを追加する](#adding-files-to-stores)
- [Failover](#failover)
- [Testing](#testing)
    - [Agents](#testing-agents)
    - [Images](#testing-images)
    - [Audio](#testing-audio)
    - [Transcriptions](#testing-transcriptions)
    - [Embeddings](#testing-embeddings)
    - [Reranking](#testing-reranking)
    - [Files](#testing-files)
    - [ベクターストア](#testing-vector-stores)
- [Events](#events)

<a name="introduction"></a>
## 導入 (Introduction)

[Laravel AI SDK](https://github.com/laravel/ai) は、OpenAI、Anthropic、Gemini などの AI プロバイダと対話するための統合された表現力豊かな API を提供します。 AI SDK を使用すると、一貫した Laravel フレンドリーなインターフェイスを使用して、ツールと構造化された出力を備えたインテリジェント エージェントの構築、画像の生成、音声の合成と転写、ベクトル埋め込みの作成などを行うことができます。

<a name="installation"></a>
## インストール (Installation)

Laravel AI SDK は Composer 経由でインストールできます。

```shell
composer require laravel/ai
```

次に、`vendor:publish` Artisan コマンドを使用して、AI SDK 構成ファイルと移行ファイルを公開する必要があります。

```shell
php artisan vendor:publish --provider="Laravel\Ai\AiServiceProvider"
```

最後に、アプリケーションのデータベース移行を実行する必要があります。これにより、AI SDK が会話ストレージを強化するために使用する `agent_conversations` テーブルと `agent_conversation_messages` テーブルが作成されます。

```shell
php artisan migrate
```

<a name="configuration"></a>
### 構成

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

テキスト、画像、オーディオ、文字起こし、埋め込みに使用されるデフォルトのモデルは、アプリケーションの `config/ai.php` 構成ファイルで構成することもできます。

<a name="custom-base-urls"></a>
### カスタムベースURL

デフォルトでは、Laravel AI SDK は各プロバイダのパブリック API エンドポイントに直接接続します。ただし、プロキシ サービスを使用して API キー管理を一元化したり、レート制限を実装したり、企業ゲートウェイ経由でトラフィックをルーティングしたりする場合など、別のエンドポイントを介してリクエストをルーティングする必要がある場合があります。

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

これは、プロキシ サービス (LiteLLM や Azure OpenAI Gateway など) を介して要求をルーティングする場合、または代替エンドポイントを使用する場合に便利です。

カスタム ベース URL は、OpenAI、Anthropic、Gemini、Groq、Cohere、DeepSeek、xAI、OpenRouter のプロバイダでサポートされています。

<a name="provider-support"></a>
### プロバイダのサポート

AI SDK は、その機能全体にわたってさまざまなプロバイダをサポートします。次の表は、各機能で利用できるプロバイダをまとめたものです。

| 特徴 | プロバイダ |
|---|---|
| 文章 | OpenAI、Anthropic、Gemini、Azure、Groq、xAI、DeepSeek、Mistral、Ollama |
| 画像 | OpenAI、Gemini、xAI |
| TTS | OpenAI、イレブンラボ |
| STT | OpenAI、イレブンラボ、ミストラル |
| 埋め込み | OpenAI、Gemini、Azure、Cohere、Mistral、Jina、VoyageAI |
| 再ランキング | コヒア、ジナ |
| ファイル | OpenAI、人類、ジェミニ |

`Laravel\Ai\Enums\Lab` 列挙型は、プレーン文字列を使用する代わりに、コード全体でプロバイダを参照するために使用できます。

```php
use Laravel\Ai\Enums\Lab;

Lab::Anthropic;
Lab::OpenAI;
Lab::Gemini;
// ...
```

<a name="agents"></a>
## エージェント (Agents)

エージェントは、Laravel AI SDK で AI プロバイダと対話するための基本的な構成要素です。各エージェントは、大規模な言語モデルと対話するために必要な命令、会話コンテキスト、ツール、出力スキーマをカプセル化する専用の PHP クラスです。エージェントは、一度構成すれば、アプリケーション全体で必要に応じてプロンプトを表示できる、セールス コーチ、ドキュメント アナライザー、サポート ボットなどの専門アシスタントと考えてください。

`make:agent` Artisan コマンドを使用してエージェントを作成できます。

```shell
php artisan make:agent SalesCoach

php artisan make:agent SalesCoach --structured
```

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
### プロンプト

エージェントにプロンプ​​トを表示するには、まず `make` メソッドまたは標準のインスタンス化を使用してインスタンスを作成し、次に `prompt` を呼び出します。

```php
$response = (new SalesCoach)
    ->prompt('Analyze this sales transcript...');

$response = SalesCoach::make()
    ->prompt('Analyze this sales transcript...');

return (string) $response;
```

`make` メソッドはコンテナからエージェントを解決し、自動依存注入を可能にします。エージェントのコンストラクターに引数を渡すこともできます。

```php
$agent = SalesCoach::make(user: $user);
```

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
### 会話のコンテキスト

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
#### 会話を思い出す

> **注意:** `RemembersConversations` トレイトを使用する前に、`vendor:publish` Artisan コマンドを使用して AI SDK 移行を公開し、実行する必要があります。これらの移行により、会話を保存するために必要なデータベース テーブルが作成されます。

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

ユーザーに対して新しい会話を開始するには、プロンプトを表示する前に `forUser` メソッドを呼び出します。

```php
$response = (new SalesCoach)->forUser($user)->prompt('Hello!');

$conversationId = $response->conversationId;
```

会話 ID は応答で返され、将来の参照のために保存したり、`agent_conversations` テーブルからユーザーのすべての会話を直接取得したりできます。

既存の会話を続行するには、`continue` メソッドを使用します。

```php
$response = (new SalesCoach)
    ->continue($conversationId, as: $user)
    ->prompt('Tell me more about that.');
```

`RemembersConversations` トレイトを使用すると、以前のメッセージが自動的にロードされ、プロンプトが表示されたときに会話コンテキストに組み込まれます。新しいメッセージ (ユーザーとアシスタントの両方) は、各対話後に自動的に保存されます。

<a name="structured-output"></a>
### 構造化された出力

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

構造化された出力を返すエージェントにプロンプ​​トを表示する場合、配列のように返された `StructuredAgentResponse` にアクセスできます。

```php
$response = (new SalesCoach)->prompt('Analyze this sales transcript...');

return $response['score'];
```

<a name="attachments"></a>
### 添付ファイル

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
### ストリーミング

`stream` メソッドを呼び出すことで、エージェントの応答をストリーミングできます。返される `StreamableAgentResponse` は、ストリーミング応答 (SSE) をクライアントに自動的に送信するルートから返される場合があります。

```php
use App\Ai\Agents\SalesCoach;

Route::get('/coach', function () {
    return (new SalesCoach)->stream('Analyze this sales transcript...');
});
```

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

あるいは、ストリーミングされたイベントを手動で反復処理することもできます。

```php
$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

foreach ($stream as $event) {
    // ...
}
```

<a name="streaming-using-the-vercel-ai-sdk-protocol"></a>
#### Vercel AI SDK プロトコルを使用したスト​​リーミング

ストリーミング可能な応答で `usingVercelDataProtocol` メソッドを呼び出すことにより、[Vercel AI SDK ストリーム プロトコル](https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocol) を使用してイベントをストリーミングできます。

```php
use App\Ai\Agents\SalesCoach;

Route::get('/coach', function () {
    return (new SalesCoach)
        ->stream('Analyze this sales transcript...')
        ->usingVercelDataProtocol();
});
```

<a name="broadcasting"></a>
### 放送

ストリーミング イベントは、いくつかの異なる方法でブロードキャストできます。まず、ストリーミング イベントで `broadcast` メソッドまたは `broadcastNow` メソッドを呼び出すだけです。

```php
use App\Ai\Agents\SalesCoach;
use Illuminate\Broadcasting\Channel;

$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

foreach ($stream as $event) {
    $event->broadcast(new Channel('channel-name'));
}
```

または、エージェントの `broadcastOnQueue` メソッドを呼び出して、エージェントの操作をキューに入れ、ストリーミング イベントが利用可能になったときにブロードキャストすることもできます。

```php
(new SalesCoach)->broadcastOnQueue(
    'Analyze this sales transcript...'
    new Channel('channel-name'),
);
```

<a name="queueing"></a>
### キューイング

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
### ツール

ツールを使用して、エージェントがプロンプトに応答する際に利用できる追加機能を提供できます。ツールは、`make:tool` Artisan コマンドを使用して作成できます。

```shell
php artisan make:tool RandomNumberGenerator
```

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
#### 類似性検索

`SimilaritySearch` ツールを使用すると、エージェントはデータベースに保存されているベクトル埋め込みを使用して、特定のクエリに類似したドキュメントを検索できます。これは、アプリケーションのデータを検索するためのアクセス権をエージェントに付与する場合の検索拡張生成 (RAG) に役立ちます。

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

最初の引数は Eloquent モデル クラスで、2 番目の引数はベクトル エンベディングを含む列です。

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

`withDescription` メソッドを使用してツールの説明をカスタマイズできます。

```php
SimilaritySearch::usingModel(Document::class, 'embedding')
    ->withDescription('Search the knowledge base for relevant articles.'),
```

<a name="provider-tools"></a>
### プロバイダツール

プロバイダ ツールは、AI プロバイダによってネイティブに実装される特別なツールで、Web 検索、URL フェッチ、ファイル検索などの機能を提供します。通常のツールとは異なり、プロバイダ ツールはアプリケーションではなくプロバイダ自体によって実行されます。

プロバイダ ツールは、エージェントの `tools` メソッドによって返されます。

<a name="web-search"></a>
#### ウェブ検索

`WebSearch` プロバイダ ツールを使用すると、エージェントは Web でリアルタイム情報を検索できます。これは、現在のイベント、最近のデータ、またはモデルのトレーニングのカットオフ以降に変更された可能性のあるトピックに関する質問に答えるのに役立ちます。

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

Web 検索ツールを構成して、検索数を制限したり、結果を特定のドメインに制限したりすることができます。

```php
(new WebSearch)->max(5)->allow(['laravel.com', 'php.net']),
```

ユーザーの場所に基づいて検索結果を絞り込むには、`location` メソッドを使用します。

```php
(new WebSearch)->location(
    city: 'New York',
    region: 'NY',
    country: 'US'
);
```

<a name="web-fetch"></a>
#### ウェブフェッチ

`WebFetch` プロバイダ ツールを使用すると、エージェントは Web ページのコンテンツをフェッチして読み取ることができます。これは、エージェントが特定の URL を分析したり、既知の Web ページから詳細情報を取得したりする必要がある場合に役立ちます。

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

Web 取得ツールを設定して、取得数を制限したり、特定のドメインに制限したりすることができます。

```php
(new WebFetch)->max(3)->allow(['docs.laravel.com']),
```

<a name="file-search"></a>
#### ファイル検索

`FileSearch` プロバイダ ツールを使用すると、エージェントは [ベクトルストア](#files) に保存されている [files](#vector-stores) を検索できます。これにより、エージェントがアップロードされたドキュメントで関連情報を検索できるようになり、検索拡張生成 (RAG) が可能になります。

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

複数のベクトル ストア ID を指定して、複数のストアを検索できます。

```php
new FileSearch(stores: ['store_1', 'store_2']);
```

ファイルに [metadata](#adding-files-to-stores) がある場合は、`where` 引数を指定して検索結果をフィルタリングできます。単純な等価フィルターの場合は、配列を渡します。

```php
new FileSearch(stores: ['store_id'], where: [
    'author' => 'Taylor Otwell',
    'year' => 2026,
]);
```

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
### ミドルウェア

エージェントはミドルウェアをサポートしているため、プロンプトがプロバイダに送信される前にインターセプトして変更することができます。ミドルウェアは、`make:agent-middleware` Artisan コマンドを使用して作成できます。

```shell
php artisan make:agent-middleware LogPrompts
```

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
### 匿名エージェント

場合によっては、専用のエージェント クラスを作成せずにモデルをすばやく操作したい場合があります。 `agent` 関数を使用して、アドホックな匿名エージェントを作成できます。

```php
use function Laravel\Ai\{agent};

$response = agent(
    instructions: 'You are an expert at software development.',
    messages: [],
    tools: [],
)->prompt('Tell me about Laravel')
```

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
### エージェント構成

PHP 属性を使用して、エージェントのテキスト生成オプションを構成できます。次の属性が使用可能です。

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
## 画像 (Images)

`Laravel\Ai\Image` クラスは、`openai`、`gemini`、または `xai` プロバイダを使用してイメージを生成するために使用できます。

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')->generate();

$rawContent = (string) $image;
```

`square`、`portrait`、および `landscape` メソッドは画像のアスペクト比を制御するために使用できますが、`quality` メソッドは最終的な画像品質 (`high`、`medium`、`low`) についてモデルをガイドするために使用できます。 `timeout` メソッドを使用して、HTTP タイムアウトを秒単位で指定できます。

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')
    ->quality('high')
    ->landscape()
    ->timeout(120)
    ->generate();
```

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

生成されたイメージは、アプリケーションの `config/filesystems.php` 構成ファイルで構成されたデフォルトのディスクに簡単に保存できます。

```php
$image = Image::of('A donut sitting on the kitchen counter');

$path = $image->store();
$path = $image->storeAs('image.jpg');
$path = $image->storePublicly();
$path = $image->storePubliclyAs('image.jpg');
```

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
## オーディオ (Audio)

`Laravel\Ai\Audio` クラスは、指定されたテキストから音声を生成するために使用できます。

```php
use Laravel\Ai\Audio;

$audio = Audio::of('I love coding with Laravel.')->generate();

$rawContent = (string) $audio;
```

`male`、`female`、および `voice` メソッドを使用して、生成されるオーディオの音声を決定できます。

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->generate();

$audio = Audio::of('I love coding with Laravel.')
    ->voice('voice-id-or-name')
    ->generate();
```

同様に、`instructions` メソッドを使用して、生成されたオーディオがどのように聞こえるべきかについてモデルを動的に指導することができます。

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->instructions('Said like a pirate')
    ->generate();
```

生成されたオーディオは、アプリケーションの `config/filesystems.php` 構成ファイルで構成されたデフォルトのディスクに簡単に保存できます。

```php
$audio = Audio::of('I love coding with Laravel.')->generate();

$path = $audio->store();
$path = $audio->storeAs('audio.mp3');
$path = $audio->storePublicly();
$path = $audio->storePubliclyAs('audio.mp3');
```

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
## 転写 (Transcriptions)

`Laravel\Ai\Transcription` クラスは、指定された音声のトランスクリプトを生成するために使用できます。

```php
use Laravel\Ai\Transcription;

$transcript = Transcription::fromPath('/home/laravel/audio.mp3')->generate();
$transcript = Transcription::fromStorage('audio.mp3')->generate();
$transcript = Transcription::fromUpload($request->file('audio'))->generate();

return (string) $transcript;
```

`diarize` メソッドを使用すると、生のテキストのトランスクリプトに加えて日記化されたトランスクリプトを応答に含めることを希望することを示すことができ、これにより、話者ごとにセグメント化されたトランスクリプトにアクセスできるようになります。

```php
$transcript = Transcription::fromStorage('audio.mp3')
    ->diarize()
    ->generate();
```

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
## 埋め込み (Embeddings)

Laravel の `Stringable` クラスから利用できる新しい `toEmbeddings` メソッドを使用すると、任意の文字列のベクトル埋め込みを簡単に生成できます。

```php
use Illuminate\Support\Str;

$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

あるいは、`Embeddings` クラスを使用して、複数の入力の埋め込みを一度に生成することもできます。

```php
use Laravel\Ai\Embeddings;

$response = Embeddings::for([
    'Napa Valley has great wine.',
    'Laravel is a PHP framework.',
])->generate();

$response->embeddings; // [[0.123, 0.456, ...], [0.789, 0.012, ...]]
```

埋め込みのディメンションとプロバイダを指定できます。

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->dimensions(1536)
    ->generate(Lab::OpenAI, 'text-embedding-3-small');
```

<a name="querying-embeddings"></a>
### 埋め込みのクエリ

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

類似性検索を高速化するためにベクトル インデックスを追加することもできます。ベクトル列で `index` を呼び出すと、Laravel はコサイン距離を使用して HNSW インデックスを自動的に作成します。

```php
$table->vector('embedding', dimensions: 1536)->index();
```

Eloquent モデルでは、ベクトル列を `array` にキャストする必要があります。

```php
protected function casts(): array
{
    return [
        'embedding' => 'array',
    ];
}
```

同様のレコードをクエリするには、`whereVectorSimilarTo` メソッドを使用します。このメソッドは、最小のコサイン類似度 (`0.0` と `1.0` の間、`1.0` は同一) によって結果をフィルターし、類似度によって結果を並べ替えます。

```php
use App\Models\Document;

$documents = Document::query()
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

`$queryEmbedding` は、浮動小数点数の配列またはプレーン文字列の場合があります。文字列が指定されると、Laravel はその文字列の埋め込みを自動的に生成します。

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', 'best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

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

エージェントにツールとして類似性検索を実行できるようにしたい場合は、[類似性検索](#similarity-search) ツールのドキュメントを確認してください。

> [!NOTE]
> 現在、ベクター クエリは、`pgvector` 拡張機能を使用した PostgreSQL 接続でのみサポートされています。

<a name="caching-embeddings"></a>
### 埋め込みのキャッシュ

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

キャッシュが有効になっている場合、埋め込みは 30 日間キャッシュされます。キャッシュ キーはプロバイダ、モデル、ディメンション、および入力コンテンツに基づいており、異なる構成で新しい埋め込みが生成される一方で、同一のリクエストがキャッシュされた結果を返すことが保証されます。

グローバル キャッシュが無効になっている場合でも、`cache` メソッドを使用して特定のリクエストのキャッシュを有効にすることもできます。

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache()
    ->generate();
```

カスタムのキャッシュ期間を秒単位で指定できます。

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache(seconds: 3600) // Cache for 1 hour
    ->generate();
```

`toEmbeddings` Stringable メソッドは、`cache` 引数も受け入れます。

```php
// Cache with default duration...
$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: true);

// Cache for a specific duration...
$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: 3600);
```

<a name="reranking"></a>
## 再ランキング (Reranking)

再ランキングを使用すると、特定のクエリとの関連性に基づいてドキュメントのリストを並べ替えることができます。これは、意味的理解を使用して検索結果を改善するのに役立ちます。

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

`limit` メソッドを使用して、返される結果の数を制限できます。

```php
$response = Reranking::of($documents)
    ->limit(5)
    ->rerank('search query');
```

<a name="reranking-collections"></a>
### コレクションの再ランキング

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
## ファイル (Files)

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

未加工のコンテンツやアップロードされたファイルを保存することもできます。

```php
use Laravel\Ai\Files;
use Laravel\Ai\Files\Document;

// Store raw content...
$stored = Document::fromString('Hello, World!', 'text/plain')->put();

// Store an uploaded file...
$stored = Document::fromUpload($request->file('document'))->put();
```

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

以前に保存されたファイルを取得するには、ファイル インスタンスで `get` メソッドを使用します。

```php
use Laravel\Ai\Files\Document;

$file = Document::fromId('file-id')->get();

$file->id;
$file->mimeType();
```

プロバイダからファイルを削除するには、`delete` メソッドを使用します。

```php
Document::fromId('file-id')->delete();
```

デフォルトでは、`Files` クラスは、アプリケーションの `config/ai.php` 構成ファイルで構成されたデフォルトの AI プロバイダを使用します。ほとんどの操作では、`provider` 引数を使用して別のプロバイダを指定できます。

```php
$response = Document::fromPath(
    '/home/laravel/document.pdf'
)->put(provider: Lab::Anthropic);
```

<a name="using-stored-files-in-conversations"></a>
### 保存されたファイルを会話で使用する

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
## ベクターストア (Vector Stores)

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

既存のベクター ストアを ID で取得するには、`get` メソッドを使用します。

```php
use Laravel\Ai\Stores;

$store = Stores::get('store_id');

$store->id;
$store->name;
$store->fileCounts;
$store->ready;
```

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
### ストアにファイルを追加する

ベクター ストアを作成したら、`add` メソッドを使用してそれに [files](#files) を追加できます。ストアに追加されたファイルは、[ファイル検索プロバイダツール](#file-search) を使用したセマンティック検索のために自動的にインデックス付けされます。

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

ファイルをストアに追加するときに、ファイルにメタデータを添付できます。このメタデータは、後で [ファイル検索プロバイダツール](#file-search) を使用するときに検索結果をフィルタリングするために使用できます。

```php
$store->add(Document::fromPath('/path/to/document.pdf'), metadata: [
    'author' => 'Taylor Otwell',
    'department' => 'Engineering',
    'year' => 2026,
]);
```

ストアからファイルを削除するには、`remove` メソッドを使用します。

```php
$store->remove('file_id');
```

ベクター ストアからファイルを削除しても、プロバイダの [ファイルストレージ](#files) からは削除されません。ファイルをベクター ストアから削除し、ファイルストレージから完全に削除するには、`deleteFile` 引数を使用します。

```php
$store->remove('file_abc123', deleteFile: true);
```

<a name="failover"></a>
## フェイルオーバー (Failover)

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
## テスト (Testing)

<a name="testing-agents"></a>
### エージェント

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

すべてのエージェント呼び出しに対応する偽の応答があることを確認するには、`preventStrayPrompts` を使用できます。偽の応答が定義されていない状態でエージェントが呼び出された場合、例外がスローされます。

```php
SalesCoach::fake()->preventStrayPrompts();
```

<a name="testing-images"></a>
### 画像

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

イメージを生成した後、受信したプロンプトについてアサーションを行うことができます。

```php
Image::assertGenerated(function (ImagePrompt $prompt) {
    return $prompt->contains('sunset') && $prompt->isLandscape();
});

Image::assertNotGenerated('Missing prompt');

Image::assertNothingGenerated();
```

キューに入れられたイメージを生成するには、キューに入れられたアサーション メソッドを使用します。

```php
Image::assertQueued(
    fn (QueuedImagePrompt $prompt) => $prompt->contains('sunset')
);

Image::assertNotQueued('Missing prompt');

Image::assertNothingQueued();
```

すべてのイメージ生成に対応する偽の応答があることを確認するには、`preventStrayImages` を使用できます。偽の応答が定義されていない状態でイメージが生成された場合、例外がスローされます。

```php
Image::fake()->preventStrayImages();
```

<a name="testing-audio"></a>
### オーディオ

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

音声を生成した後、受信したプロンプトについてアサーションを行うことができます。

```php
Audio::assertGenerated(function (AudioPrompt $prompt) {
    return $prompt->contains('Hello') && $prompt->isFemale();
});

Audio::assertNotGenerated('Missing prompt');

Audio::assertNothingGenerated();
```

キューに入れられたオーディオ生成の場合は、キューに入れられたアサーション メソッドを使用します。

```php
Audio::assertQueued(
    fn (QueuedAudioPrompt $prompt) => $prompt->contains('Hello')
);

Audio::assertNotQueued('Missing prompt');

Audio::assertNothingQueued();
```

すべてのオーディオ生成に対応する偽の応答があることを確認するには、`preventStrayAudio` を使用できます。定義された偽の応答なしでオーディオが生成された場合、例外がスローされます。

```php
Audio::fake()->preventStrayAudio();
```

<a name="testing-transcriptions"></a>
### 転写

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

すべての転写生成に対応する偽の応答があることを確認するには、`preventStrayTranscriptions` を使用できます。偽の応答が定義されていない状態でトランスクリプションが生成された場合、例外がスローされます。

```php
Transcription::fake()->preventStrayTranscriptions();
```

<a name="testing-embeddings"></a>
### 埋め込み

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

すべての埋め込み生成に対応する偽の応答があることを確認するには、`preventStrayEmbeddings` を使用できます。偽の応答が定義されていない状態で埋め込みが生成された場合、例外がスローされます。

```php
Embeddings::fake()->preventStrayEmbeddings();
```

<a name="testing-reranking"></a>
### 再ランキング

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
### ファイル

ファイル操作は、`Files` クラスの `fake` メソッドを呼び出すことで偽装される可能性があります。

```php
use Laravel\Ai\Files;

Files::fake();
```

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

ファイルの削除をアサートするには、ファイル ID を渡すことができます。

```php
Files::assertDeleted('file-id');
Files::assertNotDeleted('file-id');
Files::assertNothingDeleted();
```

<a name="testing-vector-stores"></a>
### ベクターストア

ベクター ストア操作は、`Stores` クラスの `fake` メソッドを呼び出すことで偽装される可能性があります。偽装ストアは自動的に [ファイル操作](#files) も偽装します。

```php
use Laravel\Ai\Stores;

Stores::fake();
```

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

ストアの削除に対してアサートするには、ストア ID を指定できます。

```php
Stores::assertDeleted('store_id');
Stores::assertNotDeleted('other_store_id');
Stores::assertNothingDeleted();
```

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

ファイルがプロバイダの [ファイルストレージ](#files) に保存され、同じリクエスト内のベクター ストアに追加された場合、ファイルのプロバイダ ID がわからない可能性があります。この場合、クロージャを `assertAdded` メソッドに渡して、追加されたファイルのコンテンツに対してアサートできます。

```php
use Laravel\Ai\Contracts\Files\StorableFile;
use Laravel\Ai\Files\Document;

$store->add(Document::fromString('Hello, World!', 'text/plain')->as('hello.txt'));

$store->assertAdded(fn (StorableFile $file) => $file->name() === 'hello.txt');
$store->assertAdded(fn (StorableFile $file) => $file->content() === 'Hello, World!');
```

<a name="events"></a>
## イベント (Events)

Laravel AI SDK は、次のようなさまざまな [events](/docs/{{version}}/events) をディスパッチします。

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

これらのイベントのいずれかをリッスンして、AI SDK の使用情報を記録または保存できます。

