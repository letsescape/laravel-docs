# リリースノート (Release Notes)

- [バージョン管理スキーム](#versioning-scheme)
- [サポートポリシー](#support-policy)
- [Laravel13](#laravel-13)

<a name="versioning-scheme"></a>
## バージョン管理スキーム (Versioning Scheme)

Laravel とその他のファーストパーティ パッケージは [セマンティック バージョニング](https://semver.org) に従います。メジャー フレームワーク リリースは毎年 (~第 1 四半期) リリースされますが、マイナー リリースとパッチ リリースは毎週リリースされる場合があります。マイナー リリースとパッチ リリースには重大な変更が含まれてはなりません**。

Laravel のメジャーリリースには重大な変更が含まれるため、アプリケーションまたはパッケージから Laravel フレームワークまたはそのコンポーネントを参照する場合は、必ず `^13.0` などのバージョン制約を使用する必要があります。ただし、私たちは常に 1 日以内に新しいメジャー リリースに更新できるように努めています。

<a name="named-arguments"></a>
#### 名前付き引数

[名前付き引数](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) は、Laravel の下位互換性ガイドラインではカバーされていません。 Laravel コードベースを改善するために、必要に応じて関数の引数の名前を変更することもできます。したがって、Laravelメソッドを呼び出すときに名前付き引数を使用する場合は、パラメータ名が将来変更される可能性があることを理解した上で、慎重に行う必要があります。

<a name="support-policy"></a>
## サポートポリシー (Support Policy)

すべての Laravel リリースでは、バグ修正は 18 か月間提供され、セキュリティ修正は 2 年間提供されます。すべての追加ライブラリについては、最新のメジャー リリースのみがバグ修正を受けます。さらに、データベースのバージョン [Laravelによってサポートされています](/docs/{{version}}/database#introduction) を確認してください。

<div class="overflow-auto">

| バージョン | PHP(*)   | リリース             | バグ修正まで     | セキュリティ修正の期限 |
| ------- |-----------| ------------------- | ------------------- | -------------------- |
| 10      | 8.1～8.3 | 2023 年 2 月 14 日 | 2024 年 8 月 6 日    | 2025 年 2 月 4 日   |
| 11      | 8.2～8.4 | 2024 年 3 月 12 日    | 2025 年 9 月 3 日 | 2026 年 3 月 12 日     |
| 12      | 8.2～8.5 | 2025 年 2 月 24 日 | 2026 年 8 月 13 日   | 2027 年 2 月 24 日  |
| 13      | 8.3～8.5 | 2026 年 3 月 17 日    | 2027 年第 3 四半期             | 2028 年 3 月 17 日     |

</div>

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

(*) サポートされている PHP バージョン

<a name="laravel-13"></a>
## Laravel13 (Laravel 13)

Laravel 13 は、AI ネイティブのワークフロー、より強力なデフォルト、より表現力豊かな開発者 API に重点を置いて、Laravel の年次リリースのペースを継続しています。このリリースには、ファーストパーティ AI プリミティブ、JSON:API リソース、セマンティック/ベクター検索機能、キュー、キャッシュ、セキュリティ全体にわたる段階的な改善が含まれています。

<a name="minimal-breaking-changes"></a>
### 最小限の重大な変更

このリリース サイクルでは、重大な変更を最小限に抑えることに重点を置いています。その代わりに、私たちは既存のアプリケーションを壊すことなく、年間を通して継続的に生活の質を向上させることに専念してきました。

したがって、Laravel 13 リリースは、労力という点では比較的小規模なアップグレードですが、依然として実質的な新機能を提供しています。これを考慮すると、ほとんどの Laravel アプリケーションは、アプリケーション コードをあまり変更せずに Laravel 13 にアップグレードできる可能性があります。

<a name="php-8"></a>
### PHP8.3

Laravel 13.x には、最小 PHP バージョン 8.3 が必要です。

<a name="ai-sdk"></a>
### Laravel AI SDK

Laravel 13 では、ファーストパーティの [Laravel AI SDK](https://laravel.com/ai) が導入され、テキスト生成、ツール呼び出しエージェント、埋め込み、オーディオ、画像、ベクターストア統合のための統合 API が提供されます。

AI SDK を使用すると、一貫した Laravel ネイティブの開発者エクスペリエンスを維持しながら、プロバイダに依存しない AI 機能を構築できます。

たとえば、基本エージェントは 1 回の呼び出しでプロンプトを表示できます。

```php
use App\Ai\Agents\SalesCoach;

$response = SalesCoach::make()->prompt('Analyze this sales transcript...');

return (string) $response;
```

Laravel AI SDK は、画像、音声、埋め込みも生成できます。

ビジュアル生成のユースケースのために、SDK は平易な言語のプロンプトから画像を作成するためのクリーンな API を提供します。

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')->generate();

$rawContent = (string) $image;
```

音声エクスペリエンスについては、アシスタント、ナレーション、アクセシビリティ機能用に、テキストから自然な音声を合成できます。

```php
use Laravel\Ai\Audio;

$audio = Audio::of('I love coding with Laravel.')->generate();

$rawContent = (string) $audio;
```

また、セマンティック検索および取得ワークフローの場合は、文字列から直接埋め込みを生成できます。

```php
use Illuminate\Support\Str;

$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

<a name="json-api"></a>
### JSON:API リソース

Laravel にはファーストパーティの [JSON:API リソース](/docs/{{version}}/eloquent-resources#jsonapi-resources) が含まれるようになり、JSON:API 仕様に準拠した応答を簡単に返すことができるようになりました。

JSON:API リソースは、リソース オブジェクトのシリアル化、リレーションシップの包含、スパース フィールドセット、リンク、および JSON:API 準拠の応答ヘッダーを処理します。

<a name="request-forgery-protection"></a>
### 偽造防止のリクエスト

セキュリティのために、Laravel の [偽造防止をリクエストする](/docs/{{version}}/csrf#preventing-csrf-requests) ミドルウェアが強化され、`PreventRequestForgery` として正式化され、トークンベースの CSRF 保護との互換性を維持しながらオリジン認識リクエスト検証が追加されました。

<a name="queue-routing"></a>
### キュールーティング

Laravel 13 では、`Queue::route(...)` 経由で [クラスごとのキュールーティング](/docs/{{version}}/queues#queue-routing) が追加され、特定のジョブのデフォルトのキュー/接続ルーティング ルールを中央の場所で定義できるようになります。

```php
Queue::route(ProcessPodcast::class, connection: 'redis', queue: 'podcasts');
```

<a name="php-attributes"></a>
### 拡張された PHP 属性

Laravel 13 では、ファーストパーティ PHP 属性のサポートをフレームワーク全体に拡張し続け、一般的な設定と動作に関する懸念をより宣言的にし、クラスやメソッドと同じ場所に配置できるようにします。

注目すべき追加機能には、[`#[Middleware]`](/docs/{{version}}/controllers#controller-middleware) や [`#[Authorize]`](/docs/{{version}}/controllers#authorization-attributes) などのコントローラ属性と承認属性、および [`#[Tries]`](/docs/{{version}}/queues#max-job-attempts-and-timeout)、[`#[Backoff]`](/docs/{{version}}/queues#dealing-with-failed-jobs)、[`#[Timeout]`](/docs/{{version}}/queues#max-job-attempts-and-timeout)、[`#[FailOnTimeout]`](/docs/{{version}}/queues#failing-on-timeout) などのキュー指向のジョブ コントロールが含まれます。

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

Eloquent、イベント、通知、検証、テスト、リソース シリアル化 API 全体に追加の属性も導入されており、フレームワークのより多くの領域で一貫した属性優先のオプションが提供されます。

<a name="cache-touch"></a>
### キャッシュTTL拡張

Laravel には [`Cache::touch(...)`](/docs/{{version}}/cache) が含まれるようになりました。これにより、値を取得して再保存せずに、既存のキャッシュ項目の TTL を拡張できます。

<a name="semantic-search"></a>
### セマンティック/ベクトル検索

Laravel 13 では、ネイティブ ベクター クエリのサポート、ワークフローの埋め込み、および [search](/docs/{{version}}/search#semantic-vector-search)、[queries](/docs/{{version}}/queries#vector-similarity-clauses)、および [AI SDK](/docs/{{version}}/ai-sdk#embeddings) に文書化された関連 API によって、セマンティック検索ストーリーがさらに深まりました。

これらの機能により、文字列から直接生成された埋め込みに対する類似性検索など、PostgreSQL + `pgvector` を使用した AI を活用した検索エクスペリエンスを簡単に構築できます。

たとえば、セマンティック類似性検索をクエリビルダから直接実行できます。

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', 'Best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

