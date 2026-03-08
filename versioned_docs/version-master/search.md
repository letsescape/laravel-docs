# 검색 (Search)

- [소개](#introduction)
    - [전문 검색 (Full-Text Search)](#introduction-full-text-search)
    - [시맨틱 / 벡터 검색 (Semantic / Vector Search)](#introduction-semantic-vector-search)
    - [재정렬 (Reranking)](#introduction-reranking)
    - [Scout 검색 엔진 (Scout Search Engines)](#introduction-scout-search-engines)
- [전문 검색](#full-text-search)
    - [전문 인덱스 추가](#adding-full-text-indexes)
    - [전문 검색 쿼리 실행](#running-full-text-queries)
- [시맨틱 / 벡터 검색](#semantic-vector-search)
    - [임베딩 생성](#generating-embeddings)
    - [벡터 저장 및 인덱싱](#storing-and-indexing-vectors)
    - [유사도 기반 쿼리](#querying-by-similarity)
- [결과 재정렬](#reranking-results)
- [Laravel Scout](#laravel-scout)
    - [데이터베이스 엔진](#database-engine)
    - [서드파티 엔진](#third-party-engines)
- [기법 결합](#combining-techniques)

<a name="introduction"></a>
## 소개 (Introduction)

거의 모든 애플리케이션에는 검색 기능이 필요합니다. 사용자가 지식 베이스에서 관련 문서를 찾거나, 제품 카탈로그를 탐색하거나, 문서 모음에 대해 자연어 질문을 할 때 Laravel은 이러한 각 시나리오를 처리할 수 있는 내장 도구를 제공합니다. 대부분의 경우 외부 서비스를 사용하지 않아도 충분합니다.

대부분의 애플리케이션에서는 Laravel이 제공하는 **데이터베이스 기반 검색 기능**만으로도 충분합니다. 오타 허용(typo tolerance), 패싯 필터링(faceted filtering), 대규모 지리 기반 검색(geo-search)과 같은 기능이 필요한 경우에만 외부 검색 서비스를 고려하면 됩니다.

<a name="introduction-full-text-search"></a>
#### 전문 검색 (Full-Text Search)

검색어와 얼마나 잘 일치하는지에 따라 결과의 **관련성 점수(relevance score)**를 계산하고 정렬해야 할 때, Laravel의 `whereFullText` 쿼리 빌더 메서드를 사용할 수 있습니다. 이 메서드는 MariaDB, MySQL, PostgreSQL의 **네이티브 전문 인덱스(full-text index)**를 활용합니다.

전문 검색은 단어 경계(word boundaries)와 어근 분석(stemming)을 이해합니다. 예를 들어 `"running"`을 검색하면 `"run"`이 포함된 레코드도 찾을 수 있습니다. 별도의 외부 서비스는 필요하지 않습니다.

<a name="introduction-semantic-vector-search"></a>
#### 시맨틱 / 벡터 검색 (Semantic / Vector Search)

AI 기반 **시맨틱 검색(semantic search)**은 정확한 키워드가 아닌 **의미(meaning)**를 기준으로 결과를 찾습니다. 이를 위해 `whereVectorSimilarTo` 쿼리 빌더 메서드는 PostgreSQL의 `pgvector` 확장을 사용하여 저장된 **벡터 임베딩(vector embeddings)**을 활용합니다.

예를 들어 `"best wineries in Napa Valley"`를 검색하면 단어가 직접적으로 겹치지 않더라도 `"Top Vineyards to Visit"`이라는 제목의 글을 결과로 보여줄 수 있습니다.

벡터 검색을 사용하려면 다음이 필요합니다.

- `pgvector` 확장이 설치된 PostgreSQL
- [Laravel AI SDK](/docs/master/ai-sdk)

<a name="introduction-reranking"></a>
#### 재정렬 (Reranking)

Laravel의 [AI SDK](/docs/master/ai-sdk)는 AI 모델을 사용하여 검색 결과를 **시맨틱 관련성** 기준으로 다시 정렬하는 **reranking 기능**을 제공합니다.

이 기능은 특히 **빠른 초기 검색 단계 이후의 두 번째 단계**로 사용할 때 매우 강력합니다. 예를 들어 전문 검색으로 빠르게 후보 결과를 찾은 뒤, reranking을 통해 의미적으로 가장 관련성이 높은 결과를 상위에 배치할 수 있습니다. 이렇게 하면 **속도와 정확성을 동시에 확보**할 수 있습니다.

<a name="introduction-scout-search-engines"></a>
#### Scout 검색 (Laravel Scout Search)

애플리케이션에서 Eloquent 모델과 **검색 인덱스를 자동으로 동기화**하고 싶다면 [Laravel Scout](/docs/master/scout)를 사용할 수 있습니다.

Scout는 `Searchable` 트레이트를 제공하며 다음과 같은 검색 엔진을 지원합니다.

- 내장 데이터베이스 엔진
- Algolia
- Meilisearch
- Typesense

<a name="full-text-search"></a>
## 전문 검색 (Full-Text Search)

`LIKE` 쿼리는 단순한 문자열 포함 검색에는 유용하지만 **언어 구조를 이해하지 못합니다**.

예를 들어 `"running"`을 `LIKE`로 검색하면 `"run"`이 포함된 레코드는 찾지 못합니다. 또한 결과의 **관련성에 따라 정렬되지 않고**, 데이터베이스가 발견한 순서대로 반환됩니다.

전문 검색은 다음과 같은 문제를 해결합니다.

- 단어 경계 이해
- 어근 분석(stemming)
- 관련성 점수 기반 정렬

MariaDB, MySQL, PostgreSQL에는 **빠른 전문 검색 기능이 기본적으로 내장**되어 있으므로 외부 검색 서비스가 필요하지 않습니다.

사용 방법은 다음과 같습니다.

1. 검색할 컬럼에 **전문 인덱스(full-text index)**를 추가합니다.
2. `whereFullText` 쿼리 빌더 메서드를 사용해 검색합니다.

> [!WARNING]
> 전문 검색은 현재 MariaDB, MySQL, PostgreSQL에서 지원됩니다.

<a name="adding-full-text-indexes"></a>
### 전문 인덱스 추가

전문 검색을 사용하려면 먼저 검색할 컬럼에 **전문 인덱스**를 추가해야 합니다.

단일 컬럼에 추가할 수도 있고, 여러 컬럼을 배열로 전달하여 **복합 인덱스(composite index)**를 만들 수도 있습니다.

```php
Schema::create('articles', function (Blueprint $table) {
    $table->id();
    $table->string('title');
    $table->text('body');
    $table->timestamps();

    $table->fullText(['title', 'body']);
});
```

PostgreSQL에서는 인덱스에 사용할 **언어 설정(language configuration)**을 지정할 수 있습니다. 이 설정은 단어의 어근 분석 방식에 영향을 줍니다.

```php
$table->fullText('body')->language('english');
```

인덱스 생성에 대한 자세한 내용은 [migration documentation](/docs/master/migrations#available-index-types)를 참고하십시오.

<a name="running-full-text-queries"></a>
### 전문 검색 쿼리 실행

인덱스를 생성한 후 `whereFullText` 쿼리 빌더 메서드를 사용하여 검색할 수 있습니다.

Laravel은 사용 중인 데이터베이스 드라이버에 맞는 SQL을 자동으로 생성합니다.

- MariaDB / MySQL: `MATCH(...) AGAINST(...)`
- PostgreSQL: `to_tsvector(...) @@ plainto_tsquery(...)`

```php
$articles = Article::whereFullText('body', 'web developer')->get();
```

MariaDB와 MySQL에서는 결과가 **관련성 점수 기준으로 자동 정렬**됩니다.

PostgreSQL에서는 `whereFullText`가 **검색 필터링만 수행하고 관련성 정렬은 하지 않습니다**. PostgreSQL에서 자동 관련성 정렬이 필요하다면 [Scout의 database engine](#database-engine)을 사용하는 것을 고려하십시오.

여러 컬럼에 대해 복합 전문 인덱스를 생성한 경우 동일한 컬럼 배열을 전달하여 검색할 수 있습니다.

```php
$articles = Article::whereFullText(
    ['title', 'body'], 'web developer'
)->get();
```

`orWhereFullText` 메서드를 사용하면 **OR 조건의 전문 검색**을 추가할 수 있습니다.

자세한 내용은 [query builder documentation](/docs/master/queries#full-text-where-clauses)를 참고하십시오.

<a name="semantic-vector-search"></a>
## 시맨틱 / 벡터 검색 (Semantic / Vector Search)

전문 검색은 **키워드 매칭**에 기반합니다. 즉, 검색어의 단어가 데이터에 어떤 형태로든 포함되어 있어야 합니다.

반면 **시맨틱 검색**은 완전히 다른 접근 방식을 사용합니다. AI가 생성한 **벡터 임베딩(vector embeddings)**을 사용하여 텍스트의 **의미를 숫자 배열로 표현**하고, 검색어와 의미적으로 가장 가까운 결과를 찾습니다.

예를 들어 `"best wineries in Napa Valley"`를 검색하면 `"Top Vineyards to Visit"` 같은 문서도 결과로 나타날 수 있습니다. 단어가 직접적으로 일치하지 않더라도 의미적으로 유사하기 때문입니다.

벡터 검색의 기본 흐름은 다음과 같습니다.

1. 각 콘텐츠에 대해 **임베딩(숫자 배열)**을 생성합니다.
2. 이를 데이터와 함께 저장합니다.
3. 검색 시 사용자 쿼리에 대한 임베딩을 생성합니다.
4. 벡터 공간에서 **가장 가까운 임베딩**을 찾습니다.

> [!NOTE]
> 벡터 검색을 사용하려면 `pgvector` 확장이 설치된 PostgreSQL과 [Laravel AI SDK](/docs/master/ai-sdk)가 필요합니다.  
> 모든 [Laravel Cloud](https://cloud.laravel.com) Serverless Postgres 데이터베이스에는 이미 `pgvector`가 포함되어 있습니다.

<a name="generating-embeddings"></a>
### 임베딩 생성

임베딩은 텍스트의 의미를 표현하는 **고차원 숫자 배열**입니다. 일반적으로 수백 개에서 수천 개의 숫자로 구성됩니다.

Laravel의 `Stringable` 클래스에서 제공하는 `toEmbeddings` 메서드를 사용하여 문자열의 임베딩을 생성할 수 있습니다.

```php
use Illuminate\Support\Str;

$embedding = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

여러 입력에 대한 임베딩을 한 번에 생성하려면 `Embeddings` 클래스를 사용할 수 있습니다. 이는 **API 호출을 한 번만 수행하므로 더 효율적**입니다.

```php
use Laravel\Ai\Embeddings;

$response = Embeddings::for([
    'Napa Valley has great wine.',
    'Laravel is a PHP framework.',
])->generate();

$response->embeddings; // [[0.123, 0.456, ...], [0.789, 0.012, ...]]
```

임베딩 제공자 설정, 차원 수 설정, 캐싱 등에 대한 자세한 내용은 [AI SDK documentation](/docs/master/ai-sdk#embeddings)를 참고하십시오.

<a name="storing-and-indexing-vectors"></a>
### 벡터 저장 및 인덱싱

벡터 임베딩을 저장하려면 migration에서 `vector` 컬럼을 정의해야 합니다. 또한 임베딩 제공자가 생성하는 차원 수와 동일하게 설정해야 합니다. 예를 들어 OpenAI `text-embedding-3-small` 모델은 **1536 차원**을 사용합니다.

또한 컬럼에 `index`를 호출하여 **HNSW (Hierarchical Navigable Small World)** 인덱스를 생성해야 합니다. 이 인덱스는 대규모 데이터셋에서 **유사도 검색 속도를 크게 향상**시킵니다.

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

`Schema::ensureVectorExtensionExists` 메서드는 테이블을 생성하기 전에 PostgreSQL 데이터베이스에서 `pgvector` 확장이 활성화되어 있는지 확인합니다.

Eloquent 모델에서는 벡터 컬럼을 `array`로 캐스팅해야 합니다. 이렇게 하면 Laravel이 **PHP 배열과 데이터베이스 벡터 형식 간의 변환을 자동으로 처리**합니다.

```php
protected function casts(): array
{
    return [
        'embedding' => 'array',
    ];
}
```

벡터 컬럼과 인덱스에 대한 자세한 내용은 [migration documentation](/docs/master/migrations#available-column-types)를 참고하십시오.

<a name="querying-by-similarity"></a>
### 유사도 기반 쿼리

콘텐츠에 대한 임베딩을 저장한 후 `whereVectorSimilarTo` 메서드를 사용하여 **유사한 레코드**를 검색할 수 있습니다.

이 메서드는 다음을 수행합니다.

- 코사인 유사도(cosine similarity) 계산
- `minSimilarity` 기준 이하 결과 필터링
- 유사도 기준 자동 정렬

`minSimilarity` 값은 `0.0`부터 `1.0` 사이입니다. `1.0`은 두 벡터가 완전히 동일함을 의미합니다.

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

편의를 위해 임베딩 배열 대신 **일반 문자열을 전달해도 됩니다**. 이 경우 Laravel이 자동으로 임베딩을 생성합니다.

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', 'best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

더 세밀한 제어가 필요한 경우 다음 메서드를 사용할 수 있습니다.

- `whereVectorDistanceLessThan`
- `selectVectorDistance`
- `orderByVectorDistance`

이 메서드들은 유사도 대신 **벡터 거리(distance)**를 직접 사용하여 쿼리를 제어할 수 있게 해줍니다.

자세한 내용은 다음 문서를 참고하십시오.

- [query builder documentation](/docs/master/queries#vector-similarity-clauses)
- [AI SDK documentation](/docs/master/ai-sdk#querying-embeddings)

<a name="reranking-results"></a>
## 결과 재정렬 (Reranking Results)

**Reranking**은 AI 모델을 사용하여 검색 결과를 **쿼리와의 시맨틱 관련성 기준으로 다시 정렬하는 기술**입니다.

벡터 검색과 달리 **임베딩을 미리 저장할 필요가 없습니다**. 대신 다음을 입력으로 사용합니다.

- 쿼리
- 텍스트 콘텐츠 집합

그리고 **관련성 순서로 정렬된 결과**를 반환합니다.

이 방식은 **빠른 초기 검색 이후 두 번째 단계**로 사용할 때 특히 효과적입니다.

예:

1. 전문 검색으로 수천 개의 레코드를 **상위 50개 후보로 축소**
2. reranking으로 **가장 관련성 높은 결과를 상위에 배치**

이 패턴을 **"retrieve then rerank"**라고 합니다.

`Reranking` 클래스를 사용하면 문자열 배열을 재정렬할 수 있습니다.

```php
use Laravel\Ai\Reranking;

$response = Reranking::of([
    'Django is a Python web framework.',
    'Laravel is a PHP web application framework.',
    'React is a JavaScript library for building user interfaces.',
])->rerank('PHP frameworks');

$response->first()->document; // "Laravel is a PHP web application framework."
```

Laravel 컬렉션에는 `rerank` 매크로도 제공됩니다. 이를 사용하면 Eloquent 결과를 쉽게 재정렬할 수 있습니다.

```php
$articles = Article::all()
    ->rerank('body', 'Laravel tutorials');
```

reranking 제공자 설정과 옵션에 대한 자세한 내용은 [AI SDK documentation](/docs/master/ai-sdk#reranking)를 참고하십시오.

<a name="laravel-scout"></a>
## Laravel Scout

앞에서 설명한 검색 방식들은 모두 **코드에서 직접 호출하는 쿼리 빌더 메서드**입니다.

반면 [Laravel Scout](/docs/master/scout)는 다른 접근 방식을 사용합니다. Eloquent 모델에 `Searchable` 트레이트를 추가하면 **레코드 생성, 수정, 삭제 시 검색 인덱스를 자동으로 동기화**합니다.

즉, 별도로 인덱스 업데이트를 관리하지 않아도 **항상 검색 가능한 상태를 유지**할 수 있습니다.

<a name="database-engine"></a>
### 데이터베이스 엔진 (Database Engine)

Scout의 내장 **database engine**은 기존 데이터베이스에서 **전문 검색과 `LIKE` 검색을 수행**합니다.

외부 서비스나 추가 인프라가 필요하지 않습니다.

모델에 `Searchable` 트레이트를 추가하고 `toSearchableArray` 메서드에서 검색 가능한 컬럼을 정의하면 됩니다.

또한 PHP 속성(attributes)을 사용하여 컬럼별 검색 전략을 설정할 수 있습니다.

- `SearchUsingFullText` → 전문 인덱스 사용
- `SearchUsingPrefix` → 문자열 시작부터 일치 (`example%`)
- 속성이 없는 경우 → 기본 `LIKE` 검색 (`%example%`)

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
> 컬럼에 full-text 검색을 사용하려면 해당 컬럼에 반드시 [full-text index](/docs/master/migrations#available-index-types)가 설정되어 있어야 합니다.

트레이트를 추가한 후 `search` 메서드로 모델을 검색할 수 있습니다.

```php
$articles = Article::search('Laravel')->get();
```

Scout의 database engine은 **PostgreSQL에서도 관련성 기준 자동 정렬**을 제공합니다.

검색 요구 사항이 비교적 단순하면서 **Scout의 자동 인덱스 동기화 기능을 활용하고 싶은 경우**에 매우 적합한 선택입니다.

자세한 내용은 [Scout documentation](/docs/master/scout#database-engine)을 참고하십시오.

<a name="third-party-engines"></a>
### 서드파티 엔진 (Third-Party Engines)

Scout는 다음과 같은 외부 검색 엔진도 지원합니다.

- [Algolia](https://www.algolia.com/)
- [Meilisearch](https://www.meilisearch.com)
- [Typesense](https://typesense.org)

이러한 전용 검색 서비스는 다음과 같은 고급 기능을 제공합니다.

- 오타 허용 검색
- 패싯 필터링
- 지리 기반 검색
- 사용자 정의 랭킹 규칙

특히 **대규모 서비스**나 **검색 입력 즉시 결과를 보여주는(search-as-you-type) 경험**이 필요한 경우 유용합니다.

Scout는 모든 드라이버에 대해 **통합 API**를 제공하므로 데이터베이스 엔진에서 외부 검색 엔진으로 전환할 때 **코드 변경이 최소화**됩니다.

즉, 처음에는 데이터베이스 엔진으로 시작하고 **필요할 때 외부 서비스로 확장**할 수 있습니다.

자세한 내용은 [Scout documentation](/docs/master/scout)를 참고하십시오.

> [!NOTE]
> 많은 애플리케이션은 외부 검색 엔진이 필요하지 않습니다. 이 문서에서 설명한 내장 기능만으로도 대부분의 검색 요구 사항을 해결할 수 있습니다.

<a name="combining-techniques"></a>
## 기법 결합 (Combining Techniques)

이 문서에서 설명한 검색 기법들은 **서로 배타적이지 않습니다**. 실제로는 여러 기법을 함께 사용하는 것이 가장 좋은 결과를 제공하는 경우가 많습니다.

다음은 대표적인 두 가지 패턴입니다.

**전문 검색 + 재정렬**

전문 검색으로 빠르게 후보 데이터를 줄이고, reranking을 통해 의미 기반 관련성으로 정렬합니다.

```php
$articles = Article::query()
    ->whereFullText('body', $request->input('query'))
    ->limit(50)
    ->get()
    ->rerank('body', $request->input('query'), limit: 10);
```

이 방식은 **데이터베이스 기반 전문 검색의 속도**와 **AI 기반 관련성 정확도**를 동시에 제공합니다.

**벡터 검색 + 일반 필터**

벡터 유사도 검색과 일반 `where` 조건을 함께 사용하여 **검색 범위를 특정 레코드 집합으로 제한**할 수 있습니다.

예를 들어 팀, 카테고리, 소유자 등의 조건을 함께 적용할 수 있습니다.

```php
$documents = Document::query()
    ->where('team_id', $user->team_id)
    ->whereVectorSimilarTo('embedding', $request->input('query'))
    ->limit(10)
    ->get();
```