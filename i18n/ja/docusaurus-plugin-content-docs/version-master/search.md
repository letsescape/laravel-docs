<!-- # Search -->
# Search

- [Introduction](#introduction)
    - [Full-Text Search](#introduction-full-text-search)
    - [Semantic / Vector Search](#introduction-semantic-vector-search)
    - [Reranking](#introduction-reranking)
    - [Scout Search Engines](#introduction-scout-search-engines)
- [Full-Text Search](#full-text-search)
    - [Adding Full-Text Indexes](#adding-full-text-indexes)
    - [Running Full-Text Queries](#running-full-text-queries)
- [Semantic / Vector Search](#semantic-vector-search)
    - [Generating Embeddings](#generating-embeddings)
    - [Storing and Indexing Vectors](#storing-and-indexing-vectors)
    - [Querying by Similarity](#querying-by-similarity)
- [Reranking Results](#reranking-results)
- [Laravel Scout](#laravel-scout)
    - [Database Engine](#database-engine)
    - [Third-Party Engines](#third-party-engines)
- [Combining Techniques](#combining-techniques)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Almost every application needs search. Whether your users are searching a knowledge base for relevant articles, exploring a product catalog, or asking natural-language questions against a corpus of documents, Laravel provides built-in tools to handle each of these scenarios — and you often don't need any external services to get there. -->
ほぼすべてのアプリケーションには検索が必要です。ユーザーがナレッジベースで関連記事を検索したり、製品カタログを調べたり、ドキュメントのコーパスに対して自然言語で質問したりする場合でも、Laravel はこれらの各シナリオを処理するための組み込みツールを提供します。多くの場合、そこに到達するために外部サービスは必要ありません。

<!-- Most applications will find that the built-in database-powered options provided by Laravel are more than sufficient — external search services are only necessary when you need features like typo tolerance, faceted filtering, or geo-search at massive scale. -->
ほとんどのアプリケーションでは、Laravel が提供する組み込みのデータベースを利用したオプションで十分であることがわかります。外部の検索サービスは、タイプミスの許容、ファセット フィルタリング、または大規模な地理検索などの機能が必要な場合にのみ必要です。

<a name="introduction-full-text-search"></a>
<!-- #### Full-Text Search -->
#### Full-Text Search

<!-- When you need keyword relevance ranking — where the database scores and sorts results based on how well they match the search terms — Laravel's `whereFullText` query builder method leverages native full-text indexes on MariaDB, MySQL, and PostgreSQL. Full-text search understands word boundaries and stemming, so a search for "running" can match records containing "run". No external service is required. -->
キーワードの関連性ランキングが必要な場合、データベースは検索用語との一致度に基づいて結果をスコア付けして並べ替えます。Laravel の `whereFullText` クエリビルダ メソッドは、MariaDB、MySQL、PostgreSQL のネイティブ フルテキスト インデックスを利用します。全文検索は単語の境界とステミングを理解するため、「running」を検索すると、「run」を含むレコードと一致します。外部サービスは必要ありません。

<a name="introduction-semantic-vector-search"></a>
<!-- #### Semantic / Vector Search -->
#### Semantic / Vector Search

<!-- For AI-powered semantic search that matches results by *meaning* rather than exact keywords, the `whereVectorSimilarTo` query builder method uses vector embeddings stored in PostgreSQL with the `pgvector` extension. For example, a search for "best wineries in Napa Valley" can surface an article titled "Top Vineyards to Visit" — even though the words don't overlap. Vector search requires PostgreSQL with the `pgvector` extension and the [Laravel AI SDK](/docs/master/ai-sdk). -->
正確なキーワードではなく *意味* によって結果を照合する AI を利用したセマンティック検索の場合、`whereVectorSimilarTo` クエリビルダ メソッドは、`pgvector` 拡張子を持つ PostgreSQL に保存されたベクトル埋め込みを使用します。たとえば、「ナパバレーの最高のワイナリー」を検索すると、単語が重複していない場合でも、「訪れるべき人気のワイナリー」というタイトルの記事が表示されることがあります。ベクトル検索には、`pgvector` 拡張機能と [Laravel AI SDK](/docs/master/ai-sdk) を備えた PostgreSQL が必要です。

<a name="introduction-reranking"></a>
<!-- #### Reranking -->
#### Reranking

<!-- Laravel's [AI SDK](/docs/master/ai-sdk) provides reranking capabilities that use AI models to reorder any set of results by semantic relevance to a query. Reranking is especially powerful as a second stage after a fast initial retrieval step like full-text search — giving you both speed and semantic accuracy. -->
Laravel の [AI SDK](/docs/master/ai-sdk) は、AI モデルを使用して、クエリとの意味的な関連性によって結果セットを並べ替える再ランキング機能を提供します。再ランキングは、全文検索などの高速な初期取得ステップの後の第 2 段階として特に強力で、速度と意味の正確性の両方を実現します。

<a name="introduction-scout-search-engines"></a>
<!-- #### Laravel Scout Search -->
#### Laravel Scout Search

<!-- For applications that want a `Searchable` trait that automatically keeps search indexes in sync with Eloquent models, [Laravel Scout](/docs/master/scout) offers both a built-in database engine and drivers for third-party services like Algolia, Meilisearch, and Typesense. -->
検索インデックスを Eloquent モデルと自動的に同期させる `Searchable` トレイトが必要なアプリケーション向けに、[Laravel Scout](/docs/master/scout) は、組み込みデータベース エンジンと、Algolia、Meilisearch、Typesense などのサードパーティ サービス用のドライバの両方を提供します。

<a name="full-text-search"></a>
<!-- ## Full-Text Search -->
## Full-Text Search

<!-- While `LIKE` queries work well for simple substring matching, they don't understand language. A `LIKE` search for "running" won't find a record containing "run", and results aren't ranked by relevance — they're simply returned in whatever order the database finds them. Full-text search solves both of these problems by using specialized indexes that understand word boundaries, stemming, and relevance scoring, allowing the database to return the most relevant results first. -->
`LIKE` クエリは単純な部分文字列の一致には適切に機能しますが、言語を理解できません。 「running」を `LIKE` で検索すると、「run」を含むレコードは見つかりません。また、結果は関連性によってランク付けされず、単にデータベースが見つけた順序で返されるだけです。全文検索は、単語の境界、ステミング、関連性スコアリングを理解する特殊なインデックスを使用することでこれらの問題の両方を解決し、データベースが最も関連性の高い結果を最初に返すことができるようにします。

<!-- Fast full-text search is built into MariaDB, MySQL, and PostgreSQL — no external search service is required. You only need to add a full-text index to the columns you want to search, and then use the `whereFullText` query builder method to search against them. -->
高速全文検索は MariaDB、MySQL、PostgreSQL に組み込まれており、外部の検索サービスは必要ありません。検索する列にフルテキスト インデックスを追加し、`whereFullText` クエリビルダ メソッドを使用してそれらの列に対して検索するだけです。

> [!WARNING]
> 全文検索は現在、MariaDB、MySQL、PostgreSQL でサポートされています。

<a name="adding-full-text-indexes"></a>
<!-- ### Adding Full-Text Indexes -->
### Adding Full-Text Indexes

<!-- To use full-text search, first add a full-text index to the columns you want to search. You may add the index to a single column, or pass an array of columns to create a composite index that searches across multiple fields at once: -->
全文検索を使用するには、まず、検索する列に全文インデックスを追加します。単一の列にインデックスを追加することも、列の配列を渡して複数のフィールドを一度に検索する複合インデックスを作成することもできます。

```php
Schema::create('articles', function (Blueprint $table) {
    $table->id();
    $table->string('title');
    $table->text('body');
    $table->timestamps();

    $table->fullText(['title', 'body']);
});
```

<!-- On PostgreSQL, you may specify a language configuration for the index, which controls how words are stemmed: -->
PostgreSQL では、単語のステミング方法を制御するインデックスの言語構成を指定できます。

```php
$table->fullText('body')->language('english');
```

<!-- For more information on creating indexes, consult the [migration documentation](/docs/master/migrations#available-index-types). -->
インデックスの作成の詳細については、[migration documentation](/docs/master/migrations#available-index-types) を参照してください。

<a name="running-full-text-queries"></a>
<!-- ### Running Full-Text Queries -->
### Running Full-Text Queries

<!-- Once the index is in place, use the `whereFullText` query builder method to search against it. Laravel will generate the appropriate SQL for your database driver — for example, `MATCH(...) AGAINST(...)` on MariaDB and MySQL, and `to_tsvector(...) @@ plainto_tsquery(...)` on PostgreSQL: -->
インデックスを作成したら、`whereFullText` クエリビルダ メソッドを使用してインデックスを検索します。 Laravel は、データベース ドライバに適切な SQL を生成します。たとえば、MariaDB および MySQL では `MATCH(...) AGAINST(...)`、PostgreSQL では `to_tsvector(...) @@ plainto_tsquery(...)` です。

```php
$articles = Article::whereFullText('body', 'web developer')->get();
```

<!-- When using MariaDB and MySQL, results are automatically ordered by relevance score. On PostgreSQL, `whereFullText` filters matching records but does not order them by relevance — if you need automatic relevance ordering on PostgreSQL, consider using [Scout's database engine](#database-engine), which handles this for you. -->
MariaDB と MySQL を使用すると、結果は関連性スコアによって自動的に並べられます。 PostgreSQL では、`whereFullText` は一致するレコードをフィルタリングしますが、関連性によって順序付けはしません。PostgreSQL で関連性の自動順序付けが必要な場合は、これを処理する [Scout's database engine](#database-engine) の使用を検討してください。

<!-- If you created a composite full-text index across multiple columns, you may search against all of them by passing the same array of columns to `whereFullText`: -->
複数の列にわたって複合フルテキスト インデックスを作成した場合は、同じ列の配列を `whereFullText` に渡すことで、すべての列に対して検索できます。

```php
$articles = Article::whereFullText(
    ['title', 'body'], 'web developer'
)->get();
```

<!-- The `orWhereFullText` method may be used to add a full-text search clause as an "or" condition. For complete details, consult the [query builder documentation](/docs/master/queries#full-text-where-clauses). -->
`orWhereFullText` メソッドを使用して、全文検索句を「or」条件として追加できます。詳細については、[query builder documentation](/docs/master/queries#full-text-where-clauses) を参照してください。

<a name="semantic-vector-search"></a>
<!-- ## Semantic / Vector Search -->
## Semantic / Vector Search

<!-- Full-text search relies on matching keywords — the words in the query must appear (in some form) in the data. Semantic search takes a fundamentally different approach: it uses AI-generated vector embeddings to represent the *meaning* of text as arrays of numbers, and then finds results whose meaning is most similar to the query. For example, a search for "best wineries in Napa Valley" can surface an article titled "Top Vineyards to Visit" — even though the words don't overlap at all. -->
全文検索はキーワードの一致に依存します。クエリ内の単語はデータ内に (何らかの形式で) 出現する必要があります。セマンティック検索は根本的に異なるアプローチを採用しています。AI が生成したベクトル埋め込みを使用してテキストの「意味」を数値の配列として表現し、意味がクエリに最も似ている結果を見つけます。たとえば、「ナパバレーの最高のワイナリー」を検索すると、単語がまったく重複していないにもかかわらず、「訪れるべきトップのワイナリー」というタイトルの記事が表示されることがあります。

<!-- The basic workflow for vector search is: generate an embedding (a numeric array) for each piece of content and store it alongside your data, then at search time, generate an embedding for the user's query and find the stored embeddings that are closest to it in vector space. -->
ベクトル検索の基本的なワークフローは次のとおりです。コンテンツの各部分に対してエンベディング (数値配列) を生成し、それをデータと一緒に保存します。その後、検索時にユーザーのクエリに対してエンベディングを生成し、ベクトル空間でそれに最も近い保存されたエンベディングを検索します。

> [!NOTE]
> ベクトル検索には、`pgvector` 拡張子と [Laravel AI SDK](/docs/master/ai-sdk) を持つ PostgreSQL データベースが必要です。すべての [Laravel Cloud](https://cloud.laravel.com) サーバーレス Postgres データベースには、すでに `pgvector` が含まれています。

<a name="generating-embeddings"></a>
<!-- ### Generating Embeddings -->
### Generating Embeddings

<!-- An embedding is a high-dimensional numeric array (typically hundreds or thousands of numbers) that represents the semantic meaning of a piece of text. You may generate embeddings for a string using the `toEmbeddings` method available on Laravel's `Stringable` class: -->
埋め込みは、テキストの一部の意味を表す高次元の数値配列 (通常は数百または数千の数値) です。 Laravel の `Stringable` クラスで利用できる `toEmbeddings` メソッドを使用して、文字列の埋め込みを生成できます。

```php
use Illuminate\Support\Str;

$embedding = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

<!-- To generate embeddings for multiple inputs at once — which is more efficient than generating them one at a time since it requires only a single API call to the embedding provider — use the `Embeddings` class: -->
複数の入力の埋め込みを一度に生成するには (埋め込みプロバイダへの API 呼び出しが 1 回だけ必要なので、一度に 1 つずつ生成するより効率的です)、`Embeddings` クラスを使用します。

```php
use Laravel\Ai\Embeddings;

$response = Embeddings::for([
    'Napa Valley has great wine.',
    'Laravel is a PHP framework.',
])->generate();

$response->embeddings; // [[0.123, 0.456, ...], [0.789, 0.012, ...]]
```

<!-- For more details on configuring embedding providers, customizing dimensions, and caching, consult the [AI SDK documentation](/docs/master/ai-sdk#embeddings). -->
埋め込みプロバイダの構成、ディメンションのカスタマイズ、およびキャッシュの詳細については、[AI SDK documentation](/docs/master/ai-sdk#embeddings) を参照してください。

<a name="storing-and-indexing-vectors"></a>
<!-- ### Storing and Indexing Vectors -->
### Storing and Indexing Vectors

<!-- To store vector embeddings, define a `vector` column in your migration, specifying the number of dimensions that matches your embedding provider's output (for example, 1536 for OpenAI's `text-embedding-3-small` model). You should also call `index` on the column to create an HNSW (Hierarchical Navigable Small World) index, which dramatically speeds up similarity searches on large datasets: -->
ベクトル埋め込みを保存するには、埋め込みプロバイダの出力と一致する次元数 (たとえば、OpenAI の `text-embedding-3-small` モデルの場合は 1536) を指定して、移行で `vector` 列を定義します。また、列に対して `index` を呼び出して HNSW (Hierarchical Navigable Small World) インデックスを作成する必要があります。これにより、大規模なデータセットの類似性検索が大幅に高速化されます。

```php
Schema::ensureVectorExtensionExists();

Schema::create('documents', function (Blueprint $table) {
    $table->id();
    $table->string('title');
    $table->text('content');
    $table->vector('embedding', dimensions: 1536)->index();
    $table->timestamps();
});
```

<!-- The `Schema::ensureVectorExtensionExists` method ensures the `pgvector` extension is enabled on your PostgreSQL database before creating the table. -->
`Schema::ensureVectorExtensionExists` メソッドは、テーブルを作成する前に、PostgreSQL データベースで `pgvector` 拡張機能が有効になっていることを確認します。

<!-- On your Eloquent model, cast the vector column to an `array` so that Laravel automatically handles the conversion between PHP arrays and the database's vector format: -->
Eloquent モデルで、Laravel が PHP 配列とデータベースのベクトル形式の間の変換を自動的に処理できるように、ベクトル列を `array` にcastします。

```php
protected function casts(): array
{
    return [
        'embedding' => 'array',
    ];
}
```

<!-- For more details on vector columns and indexes, consult the [migration documentation](/docs/master/migrations#available-column-types). -->
ベクトル列とインデックスの詳細については、[migration documentation](/docs/master/migrations#available-column-types) を参照してください。

<a name="querying-by-similarity"></a>
<!-- ### Querying by Similarity -->
### Querying by Similarity

<!-- Once you have stored embeddings for your content, you can search for similar records using the `whereVectorSimilarTo` method. This method compares the given embedding against the stored vectors using cosine similarity, filters out results below the `minSimilarity` threshold, and automatically orders the results by relevance — with the most similar records first. The threshold should be a value between `0.0` and `1.0`, where `1.0` means the vectors are identical: -->
コンテンツの埋め込みを保存したら、`whereVectorSimilarTo` メソッドを使用して類似のレコードを検索できます。このメソッドは、コサイン類似度を使用して、指定された埋め込みを保存されたベクトルと比較し、`minSimilarity` しきい値を下回る結果を除外し、結果を関連性によって自動的に並べ替えます (最も類似したレコードが最初になります)。しきい値は `0.0` と `1.0` の間の値である必要があります。ここで、`1.0` はベクトルが同一であることを意味します。

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

<!-- As a convenience, when a plain string is given instead of an embedding array, Laravel will automatically generate the embedding for you using your configured embedding provider. This means you can pass the user's search query directly without manually converting it to an embedding first: -->
便宜上、埋め込み配列の代わりにプレーン文字列が指定されると、Laravel は設定された埋め込みプロバイダを使用して自動的に埋め込みを生成します。これは、最初に手動で埋め込みに変換しなくても、ユーザーの検索クエリを直接渡すことができることを意味します。

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', 'best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

<!-- For lower-level control over vector queries, the `whereVectorDistanceLessThan`, `selectVectorDistance`, and `orderByVectorDistance` methods are also available. These methods let you work directly with distance values rather than similarity scores, select the computed distance as a column in your results, or manually control the ordering. For complete details, consult the [query builder documentation](/docs/master/queries#vector-similarity-clauses) and the [AI SDK documentation](/docs/master/ai-sdk#querying-embeddings). -->
ベクトル クエリの下位レベルの制御には、`whereVectorDistanceLessThan`、`selectVectorDistance`、および `orderByVectorDistance` メソッドも使用できます。これらのメソッドを使用すると、類似性スコアではなく距離値を直接操作したり、計算された距離を結果の列として選択したり、順序を手動で制御したりできます。詳細については、[query builder documentation](/docs/master/queries#vector-similarity-clauses) および [AI SDK documentation](/docs/master/ai-sdk#querying-embeddings) を参照してください。

<a name="reranking-results"></a>
<!-- ## Reranking Results -->
## Reranking Results

<!-- Reranking is a technique where an AI model reorders a set of results by how semantically relevant each result is to a given query. Unlike vector search, which requires you to pre-compute and store embeddings, reranking works on any collection of text — it takes the raw content and the query as input and returns the items sorted by relevance. -->
再ランキングは、各結果が特定のクエリに対して意味的にどの程度関連しているかに基づいて、AI モデルが一連の結果を並べ替える手法です。エンベディングを事前に計算して保存する必要があるベクトル検索とは異なり、再ランキングはあらゆるテキストのコレクションに対して機能します。生のコンテンツとクエリを入力として受け取り、関連性によってソートされた項目を返します。

<!-- Reranking is especially powerful as a second stage after a fast initial retrieval step. For example, you might use full-text search to quickly narrow thousands of records down to the top 50 candidates, and then use reranking to put the most relevant results at the top. This "retrieve then rerank" pattern gives you both speed and semantic accuracy. -->
再ランキングは、高速な初期検索ステップの後の第 2 段階として特に強力です。たとえば、全文検索を使用して数千のレコードを上位 50 の候補にすばやく絞り込み、その後、再ランキングを使用して最も関連性の高い結果を上位に表示することができます。この「取得してから再ランク付け」パターンにより、速度と意味の正確性の両方が得られます。

<!-- You may rerank an array of strings using the `Reranking` class: -->
`Reranking` クラスを使用して、文字列の配列を再ランク付けできます。

```php
use Laravel\Ai\Reranking;

$response = Reranking::of([
    'Django is a Python web framework.',
    'Laravel is a PHP web application framework.',
    'React is a JavaScript library for building user interfaces.',
])->rerank('PHP frameworks');

$response->first()->document; // "Laravel is a PHP web application framework."
```

<!-- Laravel collections also have a `rerank` macro that accepts a field name (or closure) and a query, making it easy to rerank Eloquent results: -->
Laravel コレクションには、フィールド名 (またはクロージャ) とクエリを受け入れる `rerank` マクロもあり、Eloquent の結果を簡単に再ランク付けできます。

```php
$articles = Article::all()
    ->rerank('body', 'Laravel tutorials');
```

<!-- For complete details on configuring reranking providers and available options, consult the [AI SDK documentation](/docs/master/ai-sdk#reranking). -->
再ランキングプロバイダと利用可能なオプションの構成の詳細については、[AI SDK documentation](/docs/master/ai-sdk#reranking) を参照してください。

<a name="laravel-scout"></a>
<!-- ## Laravel Scout -->
## Laravel Scout

<!-- The search techniques described above are all query builder methods that you call directly in your code. [Laravel Scout](/docs/master/scout) takes a different approach: it provides a `Searchable` trait that you add to your Eloquent models, and Scout automatically keeps your search indexes in sync as records are created, updated, and deleted. This is particularly convenient when you want your models to always be searchable without manually managing index updates. -->
上記で説明した検索テクニックはすべて、コード内で直接呼び出すクエリビルダ メソッドです。 [Laravel Scout](/docs/master/scout) は異なるアプローチを採用しています。Eloquent モデルに追加する `Searchable` トレイトを提供し、レコードの作成、更新、削除に応じて Scout が検索インデックスの同期を自動的に維持します。これは、インデックスの更新を手動で管理せずにモデルを常に検索可能にしたい場合に特に便利です。

<a name="database-engine"></a>
<!-- ### Database Engine -->
### Database Engine

<!-- Scout's built-in database engine performs full-text and `LIKE` searches against your existing database — no external service or extra infrastructure required. Simply add the `Searchable` trait to your model and define a `toSearchableArray` method that returns the columns you want to be searchable. -->
Scout の組み込みデータベース エンジンは、既存のデータベースに対して全文検索と `LIKE` 検索を実行します。外部サービスや追加のインフラストラクチャは必要ありません。 `Searchable` 特性をモデルに追加し、検索可能にする列を返す `toSearchableArray` メソッドを定義するだけです。

<!-- You may use PHP attributes to control the search strategy for each column. `SearchUsingFullText` will use your database's full-text index, `SearchUsingPrefix` will only match from the beginning of the string (`example%`), and any columns without an attribute use a default `LIKE` strategy with wildcards on both sides (`%example%`): -->
PHP 属性を使用して、各列の検索戦略を制御できます。 `SearchUsingFullText` はデータベースのフルテキスト インデックスを使用し、`SearchUsingPrefix` は文字列の先頭からのみ一致し (`example%`)、属性のない列は両側にワイルドカードを含むデフォルトの `LIKE` 戦略を使用します (`%example%`)。

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Attributes\SearchUsingFullText;
use Laravel\Scout\Attributes\SearchUsingPrefix;
use Laravel\Scout\Searchable;

class Article extends Model
{
    use Searchable;

    #[SearchUsingPrefix(['id'])]
    #[SearchUsingFullText(['title', 'body'])]
    public function toSearchableArray(): array
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'body' => $this->body,
        ];
    }
}
```

> [!WARNING]
> 列でフルテキスト クエリ制約を使用するように指定する前に、列に [full-text index](/docs/master/migrations#available-index-types) が割り当てられていることを確認してください。

<!-- Once the trait is added, you may search your model using Scout's `search` method. Scout's database engine will automatically order results by relevance, even on PostgreSQL: -->
特性が追加されたら、Scout の `search` メソッドを使用してモデルを検索できます。 Scout のデータベース エンジンは、PostgreSQL であっても、関連性によって結果を自動的に並べ替えます。

```php
$articles = Article::search('Laravel')->get();
```

<!-- The database engine is a great choice when your search needs are moderate and you want the convenience of Scout's automatic index syncing without deploying an external service. It handles the most common search use cases well, including filtering, pagination, and soft-deleted record handling. For complete details, consult the [Scout documentation](/docs/master/scout#database-engine). -->
データベース エンジンは、検索ニーズが中程度で、外部サービスを展開せずに Scout の自動インデックス同期の利便性が必要な場合に最適です。フィルタリング、ページネーション、論理的に削除されたレコードの処理など、最も一般的な検索の使用例を適切に処理します。詳細については、[Scout documentation](/docs/master/scout#database-engine) を参照してください。

<a name="third-party-engines"></a>
<!-- ### Third-Party Engines -->
### Third-Party Engines

<!-- Scout also supports third-party search engines such as [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), and [Typesense](https://typesense.org). These dedicated search services offer advanced features like typo tolerance, faceted filtering, geo-search, and custom ranking rules — features that become important at very large scale or when you need a highly polished search-as-you-type experience. -->
Scout は、[Algolia](https://www.algolia.com/)、[Meilisearch](https://www.meilisearch.com)、[Typesense](https://typesense.org) などのサードパーティの検索エンジンもサポートしています。これらの専用検索サービスは、タイプミス許容、ファセット フィルタリング、地域検索、カスタム ランキング ルールなどの高度な機能を提供します。これらの機能は、非常に大規模な場合や、高度に洗練された入力時の検索エクスペリエンスが必要な場合に重要になります。

<!-- Since Scout provides a unified API across all of its drivers, switching from the database engine to a third-party engine later requires minimal code changes. You may start with the database engine and migrate to a third-party service only if your application's needs outgrow what the database can provide. -->
Scout はすべてのドライバにわたって統合された API を提供するため、後でデータベース エンジンからサードパーティ エンジンに切り替える場合、コードの変更は最小限で済みます。データベース エンジンから開始し、アプリケーションのニーズがデータベースで提供できる量を超える場合にのみ、サードパーティ サービスに移行できます。

<!-- For complete details on configuring third-party engines, consult the [Scout documentation](/docs/master/scout). -->
サードパーティ エンジンの構成の詳細については、[Scout documentation](/docs/master/scout) を参照してください。

> [!NOTE]
> 多くのアプリケーションは外部の検索エンジンを必要としません。このページで説明する組み込みテクニックは、ほとんどのユースケースをカバーします。

<a name="combining-techniques"></a>
<!-- ## Combining Techniques -->
## Combining Techniques

<!-- The search techniques described on this page are not mutually exclusive — combining them often produces the best results. Here are two common patterns that demonstrate how these tools work together. -->
このページで説明する検索テクニックは相互に排他的ではありません。多くの場合、これらを組み合わせることで最良の結果が得られます。これらのツールがどのように連携するかを示す 2 つの一般的なパターンを次に示します。

<!-- **Full-Text Retrieval + Reranking** -->
**全文検索 + 再ランキング**

<!-- Use full-text search to quickly narrow a large dataset down to a candidate set, then apply reranking to sort those candidates by semantic relevance. This gives you the speed of database-native full-text search with the accuracy of AI-powered relevance scoring: -->
全文検索を使用して、大規模なデータセットを候補セットにすばやく絞り込み、再ランキングを適用してそれらの候補を意味的な関連性によって並べ替えます。これにより、AI を活用した関連性スコアリングの精度を備えた、データベース ネイティブの全文検索の速度が実現します。

```php
$articles = Article::query()
    ->whereFullText('body', $request->input('query'))
    ->limit(50)
    ->get()
    ->rerank('body', $request->input('query'), limit: 10);
```

<!-- **Vector Search + Traditional Filters** -->
**ベクトル検索 + 従来のフィルター**

<!-- Combine vector similarity with standard `where` clauses to scope semantic search to a subset of records. This is useful when you want meaning-based search but need to restrict results by ownership, category, or any other attribute: -->
ベクトルの類似性と標準の `where` 句を組み合わせて、セマンティック検索の範囲をレコードのサブセットに絞ります。これは、意味ベースの検索が必要だが、所有権、カテゴリ、またはその他の属性によって結果を制限する必要がある場合に便利です。

```php
$documents = Document::query()
    ->where('team_id', $user->team_id)
    ->whereVectorSimilarTo('embedding', $request->input('query'))
    ->limit(10)
    ->get();
```

