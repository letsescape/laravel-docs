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
거의 모든 애플리케이션에는 검색 기능이 필요합니다. 사용자가 관련된 글을 찾거나, 상품 카탈로그를 탐색하거나, 자연어로 문서 집합에 질문을 하는 등 다양한 상황에서 Laravel은 이러한 시나리오를 처리할 수 있는 내장 도구를 제공합니다. 그리고 대부분의 경우, 외부 서비스를 추가하지 않고도 충분합니다.

<!-- Most applications will find that the built-in database-powered options provided by Laravel are more than sufficient — external search services are only necessary when you need features like typo tolerance, faceted filtering, or geo-search at massive scale. -->
대부분의 애플리케이션은 Laravel이 제공하는 데이터베이스 기반 내장 옵션만으로 충분합니다. 대규모에서 오탈자 허용, 파셋 필터링, 위치(geo) 기반 검색 등 특수한 기능이 필요할 때만 외부 검색 서비스를 도입하면 됩니다.

<a name="introduction-full-text-search"></a>
<!-- #### Full-Text Search -->
#### Full-Text Search

<!-- When you need keyword relevance ranking — where the database scores and sorts results based on how well they match the search terms — Laravel's `whereFullText` query builder method leverages native full-text indexes on MariaDB, MySQL, and PostgreSQL. Full-text search understands word boundaries and stemming, so a search for "running" can match records containing "run". No external service is required. -->
검색어를 얼마나 잘 일치시키는지에 따라 데이터베이스가 결과의 점수를 매기고 정렬해야 할 때에는 Laravel의 `whereFullText` 쿼리 빌더 메서드를 활용할 수 있습니다. 이 메서드는 MariaDB, MySQL, PostgreSQL의 네이티브 전문 인덱스를 사용합니다. 전문 검색은 단어 경계와 형태소 분리(어근 활용)도 이해하기 때문에, 예를 들어 "running"을 검색해도 "run"이 포함된 레코드를 찾을 수 있습니다. 별도의 외부 서비스는 필요하지 않습니다.

<a name="introduction-semantic-vector-search"></a>
<!-- #### Semantic / Vector Search -->
#### Semantic / Vector Search

<!-- For AI-powered semantic search that matches results by *meaning* rather than exact keywords, the `whereVectorSimilarTo` query builder method uses vector embeddings stored in PostgreSQL with the `pgvector` extension or MariaDB. For example, a search for "best wineries in Napa Valley" can surface an article titled "Top Vineyards to Visit" — even though the words don't overlap. Vector search requires PostgreSQL with the `pgvector` extension or MariaDB 11.7 or later, as well as the [Laravel AI SDK](/docs/13.x/ai-sdk). -->
정확한 키워드가 아니라 *의미*를 기준으로 결과를 매칭하는 AI 기반 의미 검색의 경우, `whereVectorSimilarTo` 쿼리 빌더 메서드는 `pgvector` 확장 기능이 설치된 PostgreSQL 또는 MariaDB에 저장된 벡터 임베딩을 사용합니다. 예를 들어 "best wineries in Napa Valley"를 검색하면 단어가 겹치지 않더라도 "Top Vineyards to Visit"이라는 제목의 글이 검색 결과에 표시될 수 있습니다. 벡터 검색에는 `pgvector` 확장 기능이 설치된 PostgreSQL 또는 MariaDB 11.7 이상과 [Laravel AI SDK](/docs/13.x/ai-sdk)가 필요합니다.

<a name="introduction-reranking"></a>
<!-- #### Reranking -->
#### Reranking

<!-- Laravel's [AI SDK](/docs/13.x/ai-sdk) provides reranking capabilities that use AI models to reorder any set of results by semantic relevance to a query. Reranking is especially powerful as a second stage after a fast initial retrieval step like full-text search — giving you both speed and semantic accuracy. -->
Laravel의 [AI SDK](/docs/13.x/ai-sdk)는 AI 모델을 사용해 쿼리에 대한 의미적 관련도 순으로 결과 집합을 재정렬하는 기능을 제공합니다. 재정렬 기능은 빠른 1차 검색 결과(예: 전문 검색) 이후, 관련성에 따라 결과를 다시 정렬하는 2차 처리로 사용할 때 특히 강력합니다. 이를 통해 속도와 의미 기반 정확도를 모두 얻을 수 있습니다.

<a name="introduction-scout-search-engines"></a>
<!-- #### Laravel Scout Search -->
#### Laravel Scout Search

<!-- For applications that want a `Searchable` trait that automatically keeps search indexes in sync with Eloquent models, [Laravel Scout](/docs/13.x/scout) offers both a built-in database engine and drivers for third-party services like Algolia, Meilisearch, Typesense, and Turbopuffer. -->
Eloquent 모델과 검색 인덱스를 자동으로 동기화하는 `Searchable` 트레이트가 필요한 경우, [Laravel Scout](/docs/13.x/scout)는 내장 데이터베이스 엔진과 Algolia·Meilisearch·Typesense·Turbopuffer와 같은 외부 서비스용 드라이버를 모두 제공합니다.

<a name="full-text-search"></a>
<!-- ## Full-Text Search -->
## Full-Text Search

<!-- While `LIKE` queries work well for simple substring matching, they don't understand language. A `LIKE` search for "running" won't find a record containing "run", and results aren't ranked by relevance — they're simply returned in whatever order the database finds them. Full-text search solves both of these problems by using specialized indexes that understand word boundaries, stemming, and relevance scoring, allowing the database to return the most relevant results first. -->
`LIKE` 쿼리는 단순한 부분 문자열 일치에는 적합하지만, 자연어를 제대로 이해하지 못합니다. 예를 들어 `LIKE`로 "running"을 검색해도 "run"이 포함된 레코드를 찾을 수 없고, 결과 역시 관련도 순으로 정렬되지 않습니다. 전문 검색은 단어 경계, 형태소 분석, 관련성 점수 등 언어 구조를 이해하는 특수 인덱스를 사용하므로, 가장 관련성 높은 결과를 우선적으로 반환할 수 있습니다.

<!-- Fast full-text search is built into MariaDB, MySQL, and PostgreSQL — no external search service is required. You only need to add a full-text index to the columns you want to search, and then use the `whereFullText` query builder method to search against them. -->
빠른 전문 검색은 MariaDB, MySQL, PostgreSQL에 내장되어 있습니다. 별도의 외부 검색 서비스가 필요하지 않으며, 검색하려는 컬럼에 전문 인덱스를 추가하고, `whereFullText` 쿼리 빌더 메서드만 사용하면 됩니다.

> [!WARNING]
> 전문 검색은 현재 MariaDB, MySQL, PostgreSQL에서만 지원됩니다.

<a name="adding-full-text-indexes"></a>
<!-- ### Adding Full-Text Indexes -->
### Adding Full-Text Indexes

<!-- To use full-text search, first add a full-text index to the columns you want to search. You may add the index to a single column, or pass an array of columns to create a composite index that searches across multiple fields at once: -->
전문 검색을 사용하려면, 우선 검색할 컬럼에 전문 인덱스를 추가해야 합니다. 하나의 컬럼에 인덱스를 걸 수도 있고, 여러 컬럼의 배열을 전달하여 복합 인덱스(여러 필드를 동시에 검색)를 만들 수도 있습니다.

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
PostgreSQL에서는 전문 인덱스에 사용할 언어 설정도 지정할 수 있는데, 이 설정은 단어의 형태소 분석 방식에 영향을 미칩니다.

```php
$table->fullText('body')->language('english');
```

<!-- For more information on creating indexes, consult the [migration documentation](/docs/13.x/migrations#available-index-types). -->
인덱스 생성에 대한 더 자세한 정보는 [migration documentation](/docs/13.x/migrations#available-index-types)를 참고하십시오.

<a name="running-full-text-queries"></a>
<!-- ### Running Full-Text Queries -->
### Running Full-Text Queries

<!-- Once the index is in place, use the `whereFullText` query builder method to search against it. Laravel will generate the appropriate SQL for your database driver — for example, `MATCH(...) AGAINST(...)` on MariaDB and MySQL, and `to_tsvector(...) @@ plainto_tsquery(...)` on PostgreSQL: -->
인덱스를 추가했다면, 이제 `whereFullText` 쿼리 빌더 메서드로 전문 검색을 실행할 수 있습니다. Laravel은 데이터베이스 드라이버에 맞는 SQL(MariaDB·MySQL에서는 `MATCH(...) AGAINST(...)`, PostgreSQL에서는 `to_tsvector(...) @@ plainto_tsquery(...)`)을 자동 생성합니다.

```php
$articles = Article::whereFullText('body', 'web developer')->get();
```

<!-- When using MariaDB and MySQL, results are automatically ordered by relevance score. On PostgreSQL, `whereFullText` filters matching records but does not order them by relevance — if you need automatic relevance ordering on PostgreSQL, consider using [Scout's database engine](#database-engine), which handles this for you. -->
MariaDB, MySQL에서는 결과가 자동으로 관련성 점수(relevance score) 순으로 정렬됩니다. PostgreSQL에서는 `whereFullText`가 일치하는 레코드만 필터링하고, 관련성별 자동 정렬은 적용되지 않습니다. PostgreSQL에서 자동 관련성 순 정렬이 필요하다면 [Scout's database engine](#database-engine)을 사용하는 것을 고려하세요.

<!-- If you created a composite full-text index across multiple columns, you may search against all of them by passing the same array of columns to `whereFullText`: -->
여러 컬럼에 복합 전문 인덱스를 만들었을 경우, 동일한 컬럼 배열을 `whereFullText`에 전달해 전체 컬럼을 대상으로 검색할 수 있습니다.

```php
$articles = Article::whereFullText(
    ['title', 'body'], 'web developer'
)->get();
```

<!-- The `orWhereFullText` method may be used to add a full-text search clause as an "or" condition. For complete details, consult the [query builder documentation](/docs/13.x/queries#full-text-where-clauses). -->
`orWhereFullText` 메서드를 사용하면 전문 검색 조건을 "or" 조건으로 추가할 수도 있습니다. 자세한 내용은 [query builder documentation](/docs/13.x/queries#full-text-where-clauses)를 참고하세요.

<a name="semantic-vector-search"></a>
<!-- ## Semantic / Vector Search -->
## Semantic / Vector Search

<!-- Full-text search relies on matching keywords — the words in the query must appear (in some form) in the data. Semantic search takes a fundamentally different approach: it uses AI-generated vector embeddings to represent the *meaning* of text as arrays of numbers, and then finds results whose meaning is most similar to the query. For example, a search for "best wineries in Napa Valley" can surface an article titled "Top Vineyards to Visit" — even though the words don't overlap at all. -->
전문 검색은 검색어에 포함된 키워드가 실제 데이터에(변형된 형태라도) 존재해야만 검색이 됩니다. 반면 의미 기반 검색은 AI로 생성된 벡터 임베딩(숫자 배열)로 텍스트의 '의미' 자체를 표현하고, 쿼리와 가장 비슷한 의미를 가진 결과를 찾아냅니다. 예를 들어 "best wineries in Napa Valley"를 검색했을 때, "Top Vineyards to Visit"이라는 글도 단어 자체가 겹치지 않아도 결과로 노출될 수 있습니다.

<!-- The basic workflow for vector search is: generate an embedding (a numeric array) for each piece of content and store it alongside your data, then at search time, generate an embedding for the user's query and find the stored embeddings that are closest to it in vector space. -->
벡터 검색의 기본 흐름은 다음과 같습니다: 콘텐츠마다 임베딩(숫자 배열)을 생성해 데이터와 함께 저장하고, 검색 시에는 사용자의 쿼리로 임베딩을 만들어서 저장된 임베딩과의 거리를 비교해 가장 가까운(의미가 비슷한) 결과를 찾습니다.

> [!NOTE]
> 벡터 검색에는 [Laravel AI SDK](/docs/13.x/ai-sdk)가 필요하며, PostgreSQL(`pgvector` 확장 필요), MariaDB 11.7 이상, MongoDB([Laravel MongoDB package](https://laravel.com/docs/13.x/mongodb) 필요)를 지원합니다. [Laravel Cloud](https://laravel.com/cloud)의 모든 Postgres 데이터베이스에는 `pgvector`가 이미 설치되어 있습니다.

<a name="generating-embeddings"></a>
<!-- ### Generating Embeddings -->
### Generating Embeddings

<!-- An embedding is a high-dimensional numeric array (typically hundreds or thousands of numbers) that represents the semantic meaning of a piece of text. You may generate embeddings for a string using the `toEmbeddings` method available on Laravel's `Stringable` class: -->
임베딩이란, 텍스트의 의미를 수백~수천 개의 숫자로 된 고차원 배열로 변환한 결과물입니다. Laravel의 `Stringable` 클래스의 `toEmbeddings` 메서드를 사용해 문자열로부터 임베딩을 생성할 수 있습니다.

```php
use Illuminate\Support\Str;

$embedding = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

<!-- To generate embeddings for multiple inputs at once — which is more efficient than generating them one at a time since it requires only a single API call to the embedding provider — use the `Embeddings` class: -->
여러 입력값에 대한 임베딩을 한 번에 생성하고 싶다면, 이 경우 임베딩 provider에 대한 API 호출이 1회로 줄어 훨씬 효율적이므로 `Embeddings` 클래스를 사용하세요.

```php
use Laravel\Ai\Embeddings;

$response = Embeddings::for([
    'Napa Valley has great wine.',
    'Laravel is a PHP framework.',
])->generate();

$response->embeddings; // [[0.123, 0.456, ...], [0.789, 0.012, ...]]
```

<!-- For more details on configuring embedding providers, customizing dimensions, and caching, consult the [AI SDK documentation](/docs/13.x/ai-sdk#embeddings). -->
임베딩 provider 설정, 임베딩 차원 수 사용자 지정, 캐싱 등은 [AI SDK documentation](/docs/13.x/ai-sdk#embeddings)를 참고하세요.

<a name="storing-and-indexing-vectors"></a>
<!-- ### Storing and Indexing Vectors -->
### Storing and Indexing Vectors

<!-- To store vector embeddings, define a `vector` column in your migration, specifying the number of dimensions that matches your embedding provider's output (for example, 1536 for OpenAI's `text-embedding-3-small` model). You should also call `index` on the column to create an HNSW (Hierarchical Navigable Small World) index, which dramatically speeds up similarity searches on large datasets: -->
벡터 임베딩을 저장하려면 마이그레이션에서 `vector` 컬럼 타입을 정의하고, 임베딩 provider의 출력 차원 수(예: OpenAI의 `text-embedding-3-small` 모델은 1536)에 맞춰야 합니다. 또한 이 컬럼에는 `index`를 설정해 HNSW(계층적 네비게이블 스몰 월드) 인덱스를 생성하는 것이 좋습니다. 대규모 데이터셋에서 유사도 검색 성능이 크게 향상됩니다.

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
`Schema::ensureVectorExtensionExists`는 테이블 생성 전에 PostgreSQL 데이터베이스에 `pgvector` 확장이 활성화되어 있는지 확인합니다.

<!-- On your Eloquent model, use the `AsVector` cast so that Laravel automatically handles the conversion between PHP arrays and the database's vector format: -->
Eloquent 모델에서는 `AsVector` 캐스트를 사용하면 Laravel이 PHP 배열과 데이터베이스의 벡터 포맷 간 변환을 자동으로 처리합니다.

```php
use Illuminate\Database\Eloquent\Casts\AsVector;

protected function casts(): array
{
    return [
        'embedding' => AsVector::class,
    ];
}
```

<!-- For more details on vector columns and indexes, consult the [migration documentation](/docs/13.x/migrations#available-column-types). -->
벡터 컬럼과 인덱스에 대한 자세한 내용은 [migration documentation](/docs/13.x/migrations#available-column-types)를 참고하세요.

<a name="querying-by-similarity"></a>
<!-- ### Querying by Similarity -->
### Querying by Similarity

<!-- Once you have stored embeddings for your content, you can search for similar records using the `whereVectorSimilarTo` method. This method compares the given embedding against the stored vectors using cosine similarity, filters out results below the `minSimilarity` threshold, and automatically orders the results by relevance — with the most similar records first. The threshold should be a value between `0.0` and `1.0`, where `1.0` means the vectors are identical: -->
콘텐츠에 임베딩이 저장된 이후에는, `whereVectorSimilarTo` 메서드로 유사한 레코드를 검색할 수 있습니다. 이 메서드는 입력된 임베딩과 저장된 벡터를 코사인 유사도 기준으로 비교하며, `minSimilarity` 임계값보다 낮은 결과는 제외하고, 결과는 유사도가 높은 순으로 자동 정렬됩니다. 임계값은 `0.0` ~ `1.0` 범위로, `1.0`은 벡터가 완전히 동일함을 의미합니다.

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

<!-- As a convenience, when a plain string is given instead of an embedding array, Laravel will automatically generate the embedding for you using your configured embedding provider. This means you can pass the user's search query directly without manually converting it to an embedding first: -->
편의상 임베딩 배열 대신 문자열을 바로 넘기면 Laravel이 자동으로 설정된 임베딩 provider를 사용해 쿼리 임베딩을 생성합니다. 즉, 사용자의 검색어를 직접 전달해도 수동 변환 없이 동작합니다.

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', 'best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

<!-- For lower-level control over vector queries, the `whereVectorDistanceLessThan`, `selectVectorDistance`, and `orderByVectorDistance` methods are also available. These methods let you work directly with distance values rather than similarity scores, select the computed distance as a column in your results, or manually control the ordering. For complete details, consult the [query builder documentation](/docs/13.x/queries#vector-similarity-clauses) and the [AI SDK documentation](/docs/13.x/ai-sdk#querying-embeddings). -->
벡터 쿼리를 더 세밀하게 제어하고 싶다면 `whereVectorDistanceLessThan`, `selectVectorDistance`, `orderByVectorDistance` 메서드도 제공됩니다. 이들은 유사도(score) 대신 거리 값으로 작업해서, 거리 결과를 컬럼에 포함하거나 수동 정렬이 필요할 때 사용할 수 있습니다. 자세한 내용은 [query builder documentation](/docs/13.x/queries#vector-similarity-clauses) 및 [AI SDK documentation](/docs/13.x/ai-sdk#querying-embeddings)를 참고하세요.

<a name="reranking-results"></a>
<!-- ## Reranking Results -->
## Reranking Results

<!-- Reranking is a technique where an AI model reorders a set of results by how semantically relevant each result is to a given query. Unlike vector search, which requires you to pre-compute and store embeddings, reranking works on any collection of text — it takes the raw content and the query as input and returns the items sorted by relevance. -->
재정렬은 AI 모델이 주어진 쿼리에 대해 여러 결과의 의미적 관련도를 다시 평가하고, 관련도가 높은 순서로 결과 집합을 정렬하는 기법입니다. 벡터 검색과 달리, 임베딩을 미리 저장하지 않고도 텍스트 컬렉션과 쿼리만으로 바로 동작합니다.

<!-- Reranking is especially powerful as a second stage after a fast initial retrieval step. For example, you might use full-text search to quickly narrow thousands of records down to the top 50 candidates, and then use reranking to put the most relevant results at the top. This "retrieve then rerank" pattern gives you both speed and semantic accuracy. -->
재정렬은 특히 빠른 1차 검색(예: 전문 검색) 이후 2차 관련도 정렬에 적합합니다. 예를 들어, 전문 검색으로 수천 레코드에서 상위 50건 후보만 빠르게 추린 뒤, 재정렬로 관련성이 가장 높은 결과가 상단에 오도록 만들 수 있습니다. 이런 "검색 후 재정렬(Retrieve then Rerank)" 패턴은 속도와 의미 중심 정확도를 동시에 제공합니다.

<!-- You may rerank an array of strings using the `Reranking` class: -->
문자열 배열은 `Reranking` 클래스로 재정렬할 수 있습니다.

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
Laravel 컬렉션에는 필드명(또는 클로저 함수)과 쿼리를 받아 쉽게 재정렬할 수 있는 `rerank` 매크로도 있습니다. Eloquent 결과도 쉽게 정렬할 수 있습니다.

```php
$articles = Article::all()
    ->rerank('body', 'Laravel tutorials');
```

<!-- For complete details on configuring reranking providers and available options, consult the [AI SDK documentation](/docs/13.x/ai-sdk#reranking). -->
리랭킹 provider 설정 및 옵션 등 자세한 내용은 [AI SDK documentation](/docs/13.x/ai-sdk#reranking)를 참고하세요.

<a name="laravel-scout"></a>
<!-- ## Laravel Scout -->
## Laravel Scout

<!-- The search techniques described above are all query builder methods that you call directly in your code. [Laravel Scout](/docs/13.x/scout) takes a different approach: it provides a `Searchable` trait that you add to your Eloquent models, and Scout automatically keeps your search indexes in sync as records are created, updated, and deleted. This is particularly convenient when you want your models to always be searchable without manually managing index updates. -->
위에서 소개한 검색 방식들은 코드에서 직접 쿼리 빌더 메서드를 호출해 사용하는 방법입니다. [Laravel Scout](/docs/13.x/scout)는 조금 다릅니다. Eloquent 모델에 `Searchable` 트레이트를 추가하면, Scout가 레코드 생성·수정·삭제 시 자동으로 검색 인덱스와 동기화해주기 때문에 모델이 항상 검색 가능하도록 관리가 편리합니다.

<a name="database-engine"></a>
<!-- ### Database Engine -->
### Database Engine

<!-- Scout's built-in database engine performs full-text and `LIKE` searches against your existing database — no external service or extra infrastructure required. Simply add the `Searchable` trait to your model and define a `toSearchableArray` method that returns the columns you want to be searchable. -->
Scout에는 내장 데이터베이스 엔진이 포함되어 있어, 별도의 외부 서비스나 추가 인프라 없이도 기존 데이터베이스에서 전문·`LIKE` 검색을 수행할 수 있습니다. 모델에 `Searchable` 트레이트를 추가하고, 어떤 컬럼을 검색 대상으로 삼을지 `toSearchableArray` 메서드를 정의하기만 하면 됩니다.

<!-- You may use PHP attributes to control the search strategy for each column. `SearchUsingFullText` will use your database's full-text index, `SearchUsingPrefix` will only match from the beginning of the string (`example%`), and any columns without an attribute use a default `LIKE` strategy with wildcards on both sides (`%example%`): -->
각 컬럼별로 검색 전략은 PHP 속성(어트리뷰트)으로 제어할 수 있습니다. `SearchUsingFullText`는 데이터베이스 전문 인덱스를, `SearchUsingPrefix`는 컬럼값이 검색어로 시작하는 것만(`example%`) 일치시킵니다. 속성이 없는 컬럼은 양쪽에 와일드카드(`%example%`)를 붙인 기본 `LIKE` 검색이 적용됩니다.

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
> 특정 컬럼을 전문 쿼리로 지정하려면, 해당 컬럼에 [full-text index](/docs/13.x/migrations#available-index-types)가 반드시 추가되어 있어야 합니다.

<!-- Once the trait is added, you may search your model using Scout's `search` method. Scout's database engine will automatically order results by relevance, even on PostgreSQL: -->
트레이트를 추가했다면, Scout의 `search` 메서드로 모델에서 바로 검색이 가능합니다. Scout 데이터베이스 엔진은 PostgreSQL에서도 관련도 순 자동 정렬을 지원합니다.

```php
$articles = Article::search('Laravel')->get();
```

<!-- The database engine is a great choice when your search needs are moderate and you want the convenience of Scout's automatic index syncing without deploying an external service. It handles the most common search use cases well, including filtering, pagination, and soft-deleted record handling. For complete details, consult the [Scout documentation](/docs/13.x/scout#database-engine). -->
데이터베이스 엔진은 일반적인 범위의 검색 요구에 적합하며, Scout의 인덱스 자동 동기화 편리함을 누리고자 할 때 적합합니다. 필터링, 페이지네이션, 소프트 삭제 레코드 처리 등 주요 검색 기능도 잘 지원합니다. 자세한 내용은 [Scout documentation](/docs/13.x/scout#database-engine)를 참고하세요.

<a name="third-party-engines"></a>
<!-- ### Third-Party Engines -->
### Third-Party Engines

<!-- Scout also supports third-party search engines such as [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), and [Typesense](https://typesense.org). These dedicated search services offer advanced features like typo tolerance, faceted filtering, geo-search, and custom ranking rules — features that become important at very large scale or when you need a highly polished search-as-you-type experience. -->
Scout는 [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), [Typesense](https://typesense.org) 등 외부 검색 엔진도 지원합니다. 이런 전문 검색 서비스는 오탈자 허용, 파셋 필터링, 위치 기반 검색, 사용자 맞춤 정렬 규칙 등 고급 기능을 제공하며, 대규모 또는 고성능 실시간 검색이 필요한 서비스에서 유용합니다.

<!-- Since Scout provides a unified API across all of its drivers, switching from the database engine to a third-party engine later requires minimal code changes. You may start with the database engine and migrate to a third-party service only if your application's needs outgrow what the database can provide. -->
Scout는 모든 드라이버에 대해 통일된 API를 제공하므로, 이후 외부 엔진으로 교체할 때도 코드 수정이 최소화됩니다. 처음에는 내장 데이터베이스 엔진으로 시작하고, 애플리케이션 규모가 커져 데이터베이스 한계를 넘어서면 외부 서비스로 전환해도 무방합니다.

<!-- For complete details on configuring third-party engines, consult the [Scout documentation](/docs/13.x/scout). -->
서드파티 엔진 설정 등 자세한 내용은 [Scout documentation](/docs/13.x/scout)를 참고하십시오.

> [!NOTE]
> 실제로 많은 애플리케이션은 외부 검색 엔진이 필요하지 않습니다. 이 문서의 내장 검색 방법만으로도 대부분의 경우 충분합니다.

<a name="combining-techniques"></a>
<!-- ## Combining Techniques -->
## Combining Techniques

<!-- The search techniques described on this page are not mutually exclusive — combining them often produces the best results. Here are two common patterns that demonstrate how these tools work together. -->
이 문서에 소개된 검색 기술들은 상호 배타적이 아닙니다. 상황에 따라 적절히 조합하면 최고의 결과를 얻을 수 있습니다. 대표적인 활용 패턴을 예시로 살펴보겠습니다.

<!-- **Full-Text Retrieval + Reranking** -->
**전문 검색 + 재정렬(Full-Text Retrieval + Reranking)**

<!-- Use full-text search to quickly narrow a large dataset down to a candidate set, then apply reranking to sort those candidates by semantic relevance. This gives you the speed of database-native full-text search with the accuracy of AI-powered relevance scoring: -->
대규모 데이터셋에서 전문 검색으로 빠르게 후보군을 추리고, 이후 AI 기반 재정렬로 의미적으로 가장 관련도 높은 결과를 상단에 노출합니다. 이 방식은 데이터베이스 전문 검색의 속도 + 의미 기반 정확도를 동시에 제공합니다.

```php
$articles = Article::query()
    ->whereFullText('body', $request->input('query'))
    ->limit(50)
    ->get()
    ->rerank('body', $request->input('query'), limit: 10);
```

<!-- **Vector Search + Traditional Filters** -->
**벡터 검색 + 전통적 필터(Vector Search + Traditional Filters)**

<!-- Combine vector similarity with standard `where` clauses to scope semantic search to a subset of records. This is useful when you want meaning-based search but need to restrict results by ownership, category, or any other attribute: -->
벡터 유사도 기반 검색과 일반적인 `where` 조건을 결합해, 의미 중심 검색을 하면서도 소유권, 카테고리 등의 속성으로 결과를 제한할 수 있습니다.

```php
$documents = Document::query()
    ->where('team_id', $user->team_id)
    ->whereVectorSimilarTo('embedding', $request->input('query'))
    ->limit(10)
    ->get();
```
