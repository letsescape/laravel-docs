<!-- # Release Notes -->
# Release Notes

- [Versioning Scheme](#versioning-scheme)
- [Support Policy](#support-policy)
- [Laravel 13](#laravel-13)

<a name="versioning-scheme"></a>
<!-- ## Versioning Scheme -->
## Versioning Scheme

<!-- Laravel and its other first-party packages follow [Semantic Versioning](https://semver.org). Major framework releases are released every year (~Q1), while minor and patch releases may be released as often as every week. Minor and patch releases should **never** contain breaking changes. -->
Laravel とその他のファーストパーティ パッケージは [Semantic Versioning](https://semver.org) に従います。メジャー フレームワーク リリースは毎年 (~第 1 四半期) リリースされますが、マイナー リリースとパッチ リリースは毎週リリースされる場合があります。マイナー リリースとパッチ リリースには重大な変更が含まれてはなりません**。

<!-- When referencing the Laravel framework or its components from your application or package, you should always use a version constraint such as `^13.0`, since major releases of Laravel do include breaking changes. However, we strive to always ensure you may update to a new major release in one day or less. -->
Laravel のメジャーリリースには重大な変更が含まれるため、アプリケーションまたはパッケージから Laravel フレームワークまたはそのコンポーネントを参照する場合は、必ず `^13.0` などのバージョン制約を使用する必要があります。ただし、私たちは常に 1 日以内に新しいメジャー リリースに更新できるように努めています。

<a name="named-arguments"></a>
<!-- #### Named Arguments -->
#### Named Arguments

<!-- [Named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) are not covered by Laravel's backwards compatibility guidelines. We may choose to rename function arguments when necessary in order to improve the Laravel codebase. Therefore, using named arguments when calling Laravel methods should be done cautiously and with the understanding that the parameter names may change in the future. -->
[Named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) は、Laravel の下位互換性ガイドラインではカバーされていません。 Laravel コードベースを改善するために、必要に応じて関数の引数の名前を変更することもできます。したがって、Laravelメソッドを呼び出すときに名前付き引数を使用する場合は、パラメータ名が将来変更される可能性があることを理解した上で、慎重に行う必要があります。

<a name="support-policy"></a>
<!-- ## Support Policy -->
## Support Policy

<!-- For all Laravel releases, bug fixes are provided for 18 months and security fixes are provided for 2 years. For all additional libraries, only the latest major release receives bug fixes. In addition, please review the database versions [supported by Laravel](/docs/13.x/database#introduction). -->
すべての Laravel リリースでは、バグ修正は 18 か月間提供され、セキュリティ修正は 2 年間提供されます。すべての追加ライブラリについては、最新のメジャー リリースのみがバグ修正を受けます。さらに、データベースのバージョン [supported by Laravel](/docs/13.x/database#introduction) を確認してください。

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| バージョン | PHP(*)   | リリース             | バグ修正まで     | セキュリティ修正の期限 |
| ------- |-----------| ------------------- | ------------------- | -------------------- |
| 10      | 8.1～8.3 | 2023 年 2 月 14 日 | 2024 年 8 月 6 日    | 2025 年 2 月 4 日   |
| 11      | 8.2～8.4 | 2024 年 3 月 12 日    | 2025 年 9 月 3 日 | 2026 年 3 月 12 日     |
| 12      | 8.2～8.5 | 2025 年 2 月 24 日 | 2026 年 8 月 13 日   | 2027 年 2 月 24 日  |
| 13      | 8.3～8.5 | 2026 年 3 月 17 日    | 2027 年第 3 四半期             | 2028 年 3 月 17 日     |

<!-- </div> -->
</div>

<!--
<div class="version-colors">
    <div class="end-of-life">
        <div class="color-box"></div>
        <div>End of life</div>
    </div>
    <div class="security-fixes">
        <div class="color-box"></div>
        <div>Security fixes only</div>
    </div>
</div>
-->
<div class="version-colors">
    <div class="end-of-life">
        <div class="color-box"></div>
        <div>End of life</div>
    </div>
    <div class="security-fixes">
        <div class="color-box"></div>
        <div>Security fixes only</div>
    </div>
</div>

<!-- (*) Supported PHP versions -->
(*) サポートされている PHP バージョン

<a name="laravel-13"></a>
<!-- ## Laravel 13 -->
## Laravel 13

<!-- Laravel 13 continues Laravel's annual release cadence with a focus on AI-native workflows, stronger defaults, and more expressive developer APIs. This release includes first-party AI primitives, JSON:API resources, semantic / vector search capabilities, and incremental improvements across queues, cache, and security. -->
Laravel 13 は、AI ネイティブのワークフロー、より強力なデフォルト、より表現力豊かな開発者 API に重点を置いて、Laravel の年次リリースのペースを継続しています。このリリースには、ファーストパーティ AI プリミティブ、JSON:API リソース、セマンティック/ベクター検索機能、キュー、キャッシュ、セキュリティ全体にわたる段階的な改善が含まれています。

<a name="minimal-breaking-changes"></a>
<!-- ### Minimal Breaking Changes -->
### Minimal Breaking Changes

<!-- Much of our focus during this release cycle has been minimizing breaking changes. Instead, we have dedicated ourselves to shipping continuous quality-of-life improvements throughout the year that do not break existing applications. -->
このリリース サイクルでは、重大な変更を最小限に抑えることに重点を置いています。その代わりに、私たちは既存のアプリケーションを壊すことなく、年間を通して継続的に生活の質を向上させることに専念してきました。

<!-- Therefore, the Laravel 13 release is a relatively minor upgrade in terms of effort, while still delivering substantial new capabilities. In light of this, most Laravel applications may upgrade to Laravel 13 without changing much application code. -->
したがって、Laravel 13 リリースは、労力という点では比較的小規模なアップグレードですが、依然として実質的な新機能を提供しています。これを考慮すると、ほとんどの Laravel アプリケーションは、アプリケーション コードをあまり変更せずに Laravel 13 にアップグレードできる可能性があります。

<a name="php-8"></a>
<!-- ### PHP 8.3 -->
### PHP 8.3

<!-- Laravel 13.x requires a minimum PHP version of 8.3. -->
Laravel 13.x には、最小 PHP バージョン 8.3 が必要です。

<a name="ai-sdk"></a>
<!-- ### Laravel AI SDK -->
### Laravel AI SDK

<!-- Laravel 13 introduces the first-party [Laravel AI SDK](https://laravel.com/ai), providing a unified API for text generation, tool-calling agents, embeddings, audio, images, and vector-store integrations. -->
Laravel 13 では、ファーストパーティの [Laravel AI SDK](https://laravel.com/ai) が導入され、テキスト生成、ツール呼び出しエージェント、埋め込み、オーディオ、画像、ベクターストア統合のための統合 API が提供されます。

<!-- With the AI SDK, you can build provider-agnostic AI features while keeping a consistent, Laravel-native developer experience. -->
AI SDK を使用すると、一貫した Laravel ネイティブの開発者エクスペリエンスを維持しながら、プロバイダに依存しない AI 機能を構築できます。

<!-- For example, a basic agent can be prompted with a single call: -->
たとえば、基本エージェントは 1 回の呼び出しでプロンプトを表示できます。

```php
use App\Ai\Agents\SalesCoach;

$response = SalesCoach::make()->prompt('Analyze this sales transcript...');

return (string) $response;
```

<!-- The Laravel AI SDK can also generate images, audio, and embeddings: -->
Laravel AI SDK は、画像、音声、埋め込みも生成できます。

<!-- For visual generation use cases, the SDK offers a clean API for creating images from plain-language prompts: -->
ビジュアル生成のユースケースのために、SDK は平易な言語のプロンプトから画像を作成するためのクリーンな API を提供します。

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')->generate();

$rawContent = (string) $image;
```

<!-- For voice experiences, you can synthesize natural-sounding audio from text for assistants, narrations, and accessibility features: -->
音声エクスペリエンスについては、アシスタント、ナレーション、アクセシビリティ機能用に、テキストから自然な音声を合成できます。

```php
use Laravel\Ai\Audio;

$audio = Audio::of('I love coding with Laravel.')->generate();

$rawContent = (string) $audio;
```

<!-- And for semantic search and retrieval workflows, you can generate embeddings directly from strings: -->
また、セマンティック検索および取得ワークフローの場合は、文字列から直接埋め込みを生成できます。

```php
use Illuminate\Support\Str;

$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

<a name="json-api"></a>
<!-- ### JSON:API Resources -->
### JSON:API Resources

<!-- Laravel now includes first-party [JSON:API resources](/docs/13.x/eloquent-resources#jsonapi-resources), making it straightforward to return responses compliant with the JSON:API specification. -->
Laravel にはファーストパーティの [JSON:API resources](/docs/13.x/eloquent-resources#jsonapi-resources) が含まれるようになり、JSON:API 仕様に準拠した応答を簡単に返すことができるようになりました。

<!-- JSON:API resources handle resource object serialization, relationship inclusion, sparse fieldsets, links, and JSON:API-compliant response headers. -->
JSON:API リソースは、リソース オブジェクトのシリアル化、リレーションシップの包含、スパース フィールドセット、リンク、および JSON:API 準拠の応答ヘッダーを処理します。

<a name="request-forgery-protection"></a>
<!-- ### Request Forgery Protection -->
### Request Forgery Protection

<!-- For security, Laravel's [request forgery protection](/docs/13.x/csrf#preventing-csrf-requests) middleware has been enhanced and formalized as `PreventRequestForgery`, adding origin-aware request verification while preserving compatibility with token-based CSRF protection. -->
セキュリティのために、Laravel の [request forgery protection](/docs/13.x/csrf#preventing-csrf-requests) ミドルウェアが強化され、`PreventRequestForgery` として正式化され、トークンベースの CSRF 保護との互換性を維持しながらオリジン認識リクエスト検証が追加されました。

<a name="queue-routing"></a>
<!-- ### Queue Routing -->
### Queue Routing

<!-- Laravel 13 adds [queue routing by class](/docs/13.x/queues#queue-routing) via `Queue::route(...)`, allowing you to define default queue / connection routing rules for specific jobs in a central place: -->
Laravel 13 では、`Queue::route(...)` 経由で [queue routing by class](/docs/13.x/queues#queue-routing) が追加され、特定のジョブのデフォルトのキュー/接続ルーティング ルールを中央の場所で定義できるようになります。

```php
Queue::route(ProcessPodcast::class, connection: 'redis', queue: 'podcasts');
```

<a name="php-attributes"></a>
<!-- ### Expanded PHP Attributes -->
### Expanded PHP Attributes

<!-- Laravel 13 continues to expand first-party PHP attribute support across the framework, making common configuration and behavioral concerns more declarative and colocated with your classes and methods. -->
Laravel 13 では、ファーストパーティ PHP 属性のサポートをフレームワーク全体に拡張し続け、一般的な設定と動作に関する懸念をより宣言的にし、クラスやメソッドと同じ場所に配置できるようにします。

<!-- Notable additions include controller and authorization attributes like [`#[Middleware]`](/docs/13.x/controllers#controller-middleware) and [`#[Authorize]`](/docs/13.x/controllers#authorization-attributes), as well as queue-oriented job controls like [`#[Tries]`](/docs/13.x/queues#max-job-attempts-and-timeout), [`#[Backoff]`](/docs/13.x/queues#dealing-with-failed-jobs), [`#[Timeout]`](/docs/13.x/queues#max-job-attempts-and-timeout), and [`#[FailOnTimeout]`](/docs/13.x/queues#failing-on-timeout). -->
注目すべき追加機能には、[`#[Middleware]`](/docs/13.x/controllers#controller-middleware) や [`#[Authorize]`](/docs/13.x/controllers#authorization-attributes) などのコントローラ属性と承認属性、および [`#[Tries]`](/docs/13.x/queues#max-job-attempts-and-timeout)、[`#[Backoff]`](/docs/13.x/queues#dealing-with-failed-jobs)、[`#[Timeout]`](/docs/13.x/queues#max-job-attempts-and-timeout)、[`#[FailOnTimeout]`](/docs/13.x/queues#failing-on-timeout) などのキュー指向のジョブ コントロールが含まれます。

<!-- For example, controller middleware and policy checks can now be declared directly on classes and methods: -->
たとえば、コントローラのミドルウェアとポリシーのチェックをクラスとメソッドで直接宣言できるようになりました。

```php
<?php

namespace App\Http\Controllers;

use App\Models\Comment;
use App\Models\Post;
use Illuminate\Routing\Attributes\Controllers\Authorize;
use Illuminate\Routing\Attributes\Controllers\Middleware;

#[Middleware('auth')]
class CommentController
{
    #[Middleware('subscribed')]
    #[Authorize('create', [Comment::class, 'post'])]
    public function store(Post $post)
    {
        // ...
    }
}
```

<!-- Additional attributes have also been introduced across Eloquent, events, notifications, validation, testing, and resource serialization APIs, giving you a consistent attribute-first option in more areas of the framework. -->
Eloquent、イベント、通知、検証、テスト、リソース シリアル化 API 全体に追加の属性も導入されており、フレームワークのより多くの領域で一貫した属性優先のオプションが提供されます。

<a name="cache-touch"></a>
<!-- ### Cache TTL Extension -->
### Cache TTL Extension

<!-- Laravel now includes [`Cache::touch(...)`](/docs/13.x/cache), which lets you extend an existing cache item's TTL without retrieving and re-storing its value. -->
Laravel には [`Cache::touch(...)`](/docs/13.x/cache) が含まれるようになりました。これにより、値を取得して再保存せずに、既存のキャッシュ項目の TTL を拡張できます。

<a name="semantic-search"></a>
<!-- ### Semantic / Vector Search -->
### Semantic / Vector Search

<!-- Laravel 13 deepens its semantic search story with native vector query support, embedding workflows, and related APIs documented across [search](/docs/13.x/search#semantic-vector-search), [queries](/docs/13.x/queries#vector-similarity-clauses), and the [AI SDK](/docs/13.x/ai-sdk#embeddings). -->
Laravel 13 では、ネイティブ ベクター クエリのサポート、ワークフローの埋め込み、および [search](/docs/13.x/search#semantic-vector-search)、[queries](/docs/13.x/queries#vector-similarity-clauses)、および [AI SDK](/docs/13.x/ai-sdk#embeddings) に文書化された関連 API によって、セマンティック検索ストーリーがさらに深まりました。

<!-- These features make it straightforward to build AI-powered search experiences using PostgreSQL + `pgvector`, including similarity search against embeddings generated directly from strings. -->
これらの機能により、文字列から直接生成された埋め込みに対する類似性検索など、PostgreSQL + `pgvector` を使用した AI を活用した検索エクスペリエンスを簡単に構築できます。

<!-- For example, you may run semantic similarity searches directly from the query builder: -->
たとえば、セマンティック類似性検索をクエリビルダから直接実行できます。

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', 'Best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

