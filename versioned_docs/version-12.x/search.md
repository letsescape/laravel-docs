# 검색 (Search)

- [소개](#introduction)
    - [전문(Full-Text) 검색](#introduction-full-text-search)
    - [의미 기반/벡터 검색](#introduction-semantic-vector-search)
    - [재정렬(Reranking)](#introduction-reranking)
    - [Scout 검색 엔진](#introduction-scout-search-engines)
- [전문 검색](#full-text-search)
    - [전문 인덱스 추가하기](#adding-full-text-indexes)
    - [전문 쿼리 실행하기](#running-full-text-queries)
- [의미 기반/벡터 검색](#semantic-vector-search)
    - [임베딩 생성하기](#generating-embeddings)
    - [벡터 저장 및 인덱싱](#storing-and-indexing-vectors)
    - [유사도 기반 쿼리](#querying-by-similarity)
- [결과 재정렬](#reranking-results)
- [Laravel Scout](#laravel-scout)
    - [데이터베이스 엔진](#database-engine)
    - [서드파티 엔진](#third-party-engines)
- [기술 혼합 활용하기](#combining-techniques)

<a name="introduction"></a>
## 소개 (Introduction)

거의 모든 애플리케이션에는 검색 기능이 필요합니다. 사용자가 관련된 글을 찾거나, 상품 카탈로그를 탐색하거나, 자연어로 문서 집합에 질문을 하는 등 다양한 상황에서 Laravel은 이러한 시나리오를 처리할 수 있는 내장 도구를 제공합니다. 그리고 대부분의 경우, 외부 서비스를 추가하지 않고도 충분합니다.

대부분의 애플리케이션은 Laravel이 제공하는 데이터베이스 기반 내장 옵션만으로 충분합니다. 대규모에서 오탈자 허용, 파셋 필터링, 위치(geo) 기반 검색 등 특수한 기능이 필요할 때만 외부 검색 서비스를 도입하면 됩니다.

<a name="introduction-full-text-search"></a>
#### 전문(Full-Text) 검색

검색어를 얼마나 잘 일치시키는지에 따라 데이터베이스가 결과의 점수를 매기고 정렬해야 할 때에는 Laravel의 `whereFullText` 쿼리 빌더 메서드를 활용할 수 있습니다. 이 메서드는 MariaDB, MySQL, PostgreSQL의 네이티브 전문 인덱스를 사용합니다. 전문 검색은 단어 경계와 형태소 분리(어근 활용)도 이해하기 때문에, 예를 들어 "running"을 검색해도 "run"이 포함된 레코드를 찾을 수 있습니다. 별도의 외부 서비스는 필요하지 않습니다.

<a name="introduction-semantic-vector-search"></a>
#### 의미 기반/벡터 검색

정확한 키워드가 아니라 *의미*로 결과를 매칭해야 할 땐, AI 기반 의미 검색을 사용합니다. `whereVectorSimilarTo` 쿼리 빌더 메서드는 PostgreSQL의 `pgvector` 확장 기능을 활용한 벡터 임베딩(vector embedding)을 사용합니다. 예를 들어, "best wineries in Napa Valley"를 검색하면 "Top Vineyards to Visit"라는 제목의 글도 결과로 보여줄 수 있습니다. (단어는 겹치지 않아도 의미가 비슷함.) 벡터 검색은 PostgreSQL과 `pgvector` 확장, 그리고 [Laravel AI SDK](/docs/12.x/ai-sdk)가 필요합니다.

<a name="introduction-reranking"></a>
#### 재정렬(Reranking)

Laravel의 [AI SDK](/docs/12.x/ai-sdk)는 AI 모델을 사용해 쿼리에 대한 의미적 관련도 순으로 결과 집합을 재정렬하는 기능을 제공합니다. 재정렬 기능은 빠른 1차 검색 결과(예: 전문 검색) 이후, 관련성에 따라 결과를 다시 정렬하는 2차 처리로 사용할 때 특히 강력합니다. 이를 통해 속도와 의미 기반 정확도를 모두 얻을 수 있습니다.

<a name="introduction-scout-search-engines"></a>
#### Laravel Scout 검색

Eloquent 모델과 검색 인덱스를 자동으로 동기화하는 `Searchable` 트레이트가 필요한 경우, [Laravel Scout](/docs/12.x/scout)는 내장 데이터베이스 엔진과 Algolia·Meilisearch·Typesense와 같은 외부 서비스용 드라이버를 모두 제공합니다.

<a name="full-text-search"></a>
## 전문 검색 (Full-Text Search)

`LIKE` 쿼리는 단순한 부분 문자열 일치에는 적합하지만, 자연어를 제대로 이해하지 못합니다. 예를 들어 `LIKE 'running'`으로는 "run"이 포함된 레코드를 찾을 수 없고, 결과 역시 관련도 순으로 정렬되지 않습니다. 전문 검색은 단어 경계, 형태소 분석, 관련성 점수 등 언어 구조를 이해하는 특수 인덱스를 사용하므로, 가장 관련성 높은 결과를 우선적으로 반환할 수 있습니다.

빠른 전문 검색은 MariaDB, MySQL, PostgreSQL에 내장되어 있습니다. 별도의 외부 검색 서비스가 필요하지 않으며, 검색하려는 컬럼에 전문 인덱스를 추가하고, `whereFullText` 쿼리 빌더 메서드만 사용하면 됩니다.

> [!WARNING]
> 전문 검색은 현재 MariaDB, MySQL, PostgreSQL에서만 지원됩니다.

<a name="adding-full-text-indexes"></a>
### 전문 인덱스 추가하기

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

PostgreSQL에서는 전문 인덱스에 사용할 언어 설정도 지정할 수 있는데, 이 설정은 단어의 형태소 분석 방식에 영향을 미칩니다.

```php
$table->fullText('body')->language('english');
```

인덱스 생성에 대한 더 자세한 정보는 [마이그레이션 문서](/docs/12.x/migrations#available-index-types)를 참고하십시오.

<a name="running-full-text-queries"></a>
### 전문 쿼리 실행하기

인덱스를 추가했다면, 이제 `whereFullText` 쿼리 빌더 메서드로 전문 검색을 실행할 수 있습니다. Laravel은 데이터베이스 드라이버에 맞는 SQL(MariaDB·MySQL에서는 `MATCH(...) AGAINST(...)`, PostgreSQL에서는 `to_tsvector(...) @@ plainto_tsquery(...)`)을 자동 생성합니다.

```php
$articles = Article::whereFullText('body', 'web developer')->get();
```

MariaDB, MySQL에서는 결과가 자동으로 관련성 점수(relevance score) 순으로 정렬됩니다. PostgreSQL에서는 `whereFullText`가 일치하는 레코드만 필터링하고, 관련성별 자동 정렬은 적용되지 않습니다. PostgreSQL에서 자동 관련성 순 정렬이 필요하다면 [Scout의 데이터베이스 엔진](#database-engine)을 사용하는 것을 고려하세요.

여러 컬럼에 복합 전문 인덱스를 만들었을 경우, 동일한 컬럼 배열을 `whereFullText`에 전달해 전체 컬럼을 대상으로 검색할 수 있습니다.

```php
$articles = Article::whereFullText(
    ['title', 'body'], 'web developer'
)->get();
```

`orWhereFullText` 메서드를 사용하면 전문 검색 조건을 "or" 조건으로 추가할 수도 있습니다. 자세한 내용은 [쿼리 빌더 문서](/docs/12.x/queries#full-text-where-clauses)를 참고하세요.

<a name="semantic-vector-search"></a>
## 의미 기반/벡터 검색 (Semantic / Vector Search)

전문 검색은 검색어에 포함된 키워드가 실제 데이터에(변형된 형태라도) 존재해야만 검색이 됩니다. 반면 의미 기반 검색은 AI로 생성된 벡터 임베딩(숫자 배열)로 텍스트의 '의미' 자체를 표현하고, 쿼리와 가장 비슷한 의미를 가진 결과를 찾아냅니다. 예를 들어 "best wineries in Napa Valley"를 검색했을 때, "Top Vineyards to Visit"이라는 글도 단어 자체가 겹치지 않아도 결과로 노출될 수 있습니다.

벡터 검색의 기본 흐름은 다음과 같습니다: 콘텐츠마다 임베딩(숫자 배열)을 생성해 데이터와 함께 저장하고, 검색 시에는 사용자의 쿼리로 임베딩을 만들어서 저장된 임베딩과의 거리를 비교해 가장 가까운(의미가 비슷한) 결과를 찾습니다.

> [!NOTE]
> 벡터 검색은 PostgreSQL 데이터베이스의 `pgvector` 확장과 [Laravel AI SDK](/docs/12.x/ai-sdk)가 필요합니다. [Laravel Cloud](https://cloud.laravel.com)의 Serverless Postgres 데이터베이스에는 `pgvector`가 이미 포함되어 있습니다.

<a name="generating-embeddings"></a>
### 임베딩 생성하기

임베딩이란, 텍스트의 의미를 수백~수천 개의 숫자로 된 고차원 배열로 변환한 결과물입니다. Laravel의 `Stringable` 클래스의 `toEmbeddings` 메서드를 사용해 문자열로부터 임베딩을 생성할 수 있습니다.

```php
use Illuminate\Support\Str;

$embedding = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

여러 개의 입력값에 대해 임베딩을 한 번에 생성하고 싶다면(이 경우 임베딩 제공자에 대한 API 호출이 1회로 줄어 훨씬 효율적임), `Embeddings` 클래스를 사용하세요.

```php
use Laravel\Ai\Embeddings;

$response = Embeddings::for([
    'Napa Valley has great wine.',
    'Laravel is a PHP framework.',
])->generate();

$response->embeddings; // [[0.123, 0.456, ...], [0.789, 0.012, ...]]
```

임베딩 제공자 설정, 임베딩의 차원 수 커스터마이징, 캐싱 등은 [AI SDK 문서](/docs/12.x/ai-sdk#embeddings)를 참고하세요.

<a name="storing-and-indexing-vectors"></a>
### 벡터 저장 및 인덱싱

벡터 임베딩을 저장하려면, 마이그레이션에서 `vector` 컬럼 타입을 정의하고 임베딩 제공자의 출력 차원 수(예: OpenAI의 `text-embedding-3-small` 모델은 1536)를 맞춰줘야 합니다. 이 컬럼에는 `index`를 설정해 HNSW(계층적 네비게이블 스몰 월드) 인덱스를 생성하는 것이 좋은데, 대규모 데이터셋에서 유사도 검색 시 성능이 크게 향상됩니다.

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

`Schema::ensureVectorExtensionExists`는 테이블 생성 전에 PostgreSQL 데이터베이스에 `pgvector` 확장이 활성화되어 있는지 확인합니다.

Eloquent 모델에서는 해당 벡터 컬럼을 `array`로 캐스팅하면, PHP 배열과 데이터베이스의 벡터 포맷 간 변환을 Laravel이 자동으로 처리합니다.

```php
protected function casts(): array
{
    return [
        'embedding' => 'array',
    ];
}
```

벡터 컬럼과 인덱스에 대한 자세한 내용은 [마이그레이션 문서](/docs/12.x/migrations#available-column-types)를 참고하세요.

<a name="querying-by-similarity"></a>
### 유사도 기반 쿼리

콘텐츠에 임베딩이 저장된 이후에는, `whereVectorSimilarTo` 메서드로 유사한 레코드를 검색할 수 있습니다. 이 메서드는 입력된 임베딩과 저장된 벡터를 코사인 유사도 기준으로 비교하며, `minSimilarity` 임계값보다 낮은 결과는 제외하고, 결과는 유사도가 높은 순으로 자동 정렬됩니다. 임계값은 `0.0` ~ `1.0` 범위로, `1.0`은 벡터가 완전히 동일함을 의미합니다.

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

편의 기능으로, 임베딩 배열 대신 문자열을 바로 넣으면 Laravel이 자동으로 설정된 임베딩 제공자를 통해 쿼리 임베딩을 생성합니다. 즉, 사용자의 검색어를 직접 넘겨도 수동 변환 없이 동작합니다.

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', 'best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

벡터 쿼리를 더 세밀하게 제어하고 싶다면 `whereVectorDistanceLessThan`, `selectVectorDistance`, `orderByVectorDistance` 메서드도 제공됩니다. 이들은 유사도(score) 대신 거리 값으로 작업해서, 거리 결과를 컬럼에 포함하거나 수동 정렬이 필요할 때 사용할 수 있습니다. 자세한 내용은 [쿼리 빌더 문서](/docs/12.x/queries#vector-similarity-clauses) 및 [AI SDK 문서](/docs/12.x/ai-sdk#querying-embeddings)를 참고하세요.

<a name="reranking-results"></a>
## 결과 재정렬 (Reranking Results)

재정렬은 AI 모델이 주어진 쿼리에 대해 여러 결과의 의미적 관련도를 다시 평가하고, 관련도가 높은 순서로 결과 집합을 정렬하는 기법입니다. 벡터 검색과 달리, 임베딩을 미리 저장하지 않고도 텍스트 컬렉션과 쿼리만으로 바로 동작합니다.

재정렬은 특히 빠른 1차 검색(예: 전문 검색) 이후 2차 관련도 정렬에 적합합니다. 예를 들어, 전문 검색으로 수천 레코드에서 상위 50건 후보만 빠르게 추린 뒤, 재정렬로 관련성이 가장 높은 결과가 상단에 오도록 만들 수 있습니다. 이런 "검색 후 재정렬(Retrieve then Rerank)" 패턴은 속도와 의미 중심 정확도를 동시에 제공합니다.

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

Laravel 컬렉션에는 필드명(또는 클로저 함수)과 쿼리를 받아 쉽게 재정렬할 수 있는 `rerank` 매크로도 있습니다. Eloquent 결과도 쉽게 정렬할 수 있습니다.

```php
$articles = Article::all()
    ->rerank('body', 'Laravel tutorials');
```

재정렬 제공자 설정 및 옵션 등 자세한 내용은 [AI SDK 문서](/docs/12.x/ai-sdk#reranking)를 참고하세요.

<a name="laravel-scout"></a>
## Laravel Scout

위에서 소개한 검색 방식들은 코드에서 직접 쿼리 빌더 메서드를 호출해 사용하는 방법입니다. [Laravel Scout](/docs/12.x/scout)는 조금 다릅니다. Eloquent 모델에 `Searchable` 트레이트를 추가하면, Scout가 레코드 생성·수정·삭제 시 자동으로 검색 인덱스와 동기화해주기 때문에 모델이 항상 검색 가능하도록 관리가 편리합니다.

<a name="database-engine"></a>
### 데이터베이스 엔진

Scout에는 내장 데이터베이스 엔진이 포함되어 있어, 별도의 외부 서비스나 추가 인프라 없이도 기존 데이터베이스에서 전문·LIKE 검색을 수행할 수 있습니다. 모델에 `Searchable` 트레이트를 추가하고, 어떤 컬럼을 검색 대상으로 삼을지 `toSearchableArray` 메서드를 정의하기만 하면 됩니다.

각 컬럼별로 검색 전략은 PHP 속성(어트리뷰트)으로 제어할 수 있습니다. `SearchUsingFullText`는 데이터베이스 전문 인덱스를, `SearchUsingPrefix`는 컬럼값이 검색어로 시작하는 것만(`example%`) 일치시킵니다. 속성이 없는 컬럼은 양쪽에 와일드카드(`%example%`)를 붙인 기본 LIKE 검색이 적용됩니다.

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
> 특정 컬럼을 전문 쿼리로 지정하려면, 해당 컬럼에 [전문 인덱스](/docs/12.x/migrations#available-index-types)가 반드시 추가되어 있어야 합니다.

트레이트를 추가했다면, Scout의 `search` 메서드로 모델에서 바로 검색이 가능합니다. Scout 데이터베이스 엔진은 PostgreSQL에서도 관련도 순 자동 정렬을 지원합니다.

```php
$articles = Article::search('Laravel')->get();
```

데이터베이스 엔진은 일반적인 범위의 검색 요구에 적합하며, Scout의 인덱스 자동 동기화 편리함을 누리고자 할 때 적합합니다. 필터링, 페이지네이션, 소프트 삭제 레코드 처리 등 주요 검색 기능도 잘 지원합니다. 자세한 내용은 [Scout 문서](/docs/12.x/scout#database-engine)를 참고하세요.

<a name="third-party-engines"></a>
### 서드파티 엔진

Scout는 [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), [Typesense](https://typesense.org) 등 외부 검색 엔진도 지원합니다. 이런 전문 검색 서비스는 오탈자 허용, 파셋 필터링, 위치 기반 검색, 사용자 맞춤 정렬 규칙 등 고급 기능을 제공하며, 대규모 또는 고성능 실시간 검색이 필요한 서비스에서 유용합니다.

Scout는 모든 드라이버에 대해 통일된 API를 제공하므로, 이후 외부 엔진으로 교체할 때도 코드 수정이 최소화됩니다. 처음에는 내장 데이터베이스 엔진으로 시작하고, 애플리케이션 규모가 커져 데이터베이스 한계를 넘어서면 외부 서비스로 전환해도 무방합니다.

서드파티 엔진 설정 등 자세한 내용은 [Scout 문서](/docs/12.x/scout)를 참고하십시오.

> [!NOTE]
> 실제로 많은 애플리케이션은 외부 검색 엔진이 필요하지 않습니다. 이 문서의 내장 검색 방법만으로도 대부분의 경우 충분합니다.

<a name="combining-techniques"></a>
## 기술 혼합 활용하기 (Combining Techniques)

이 문서에 소개된 검색 기술들은 상호 배타적이 아닙니다. 상황에 따라 적절히 조합하면 최고의 결과를 얻을 수 있습니다. 대표적인 활용 패턴을 예시로 살펴보겠습니다.

**전문 검색 + 재정렬(Full-Text Retrieval + Reranking)**

대규모 데이터셋에서 전문 검색으로 빠르게 후보군을 추리고, 이후 AI 기반 재정렬로 의미적으로 가장 관련도 높은 결과를 상단에 노출합니다. 이 방식은 데이터베이스 전문 검색의 속도 + 의미 기반 정확도를 동시에 제공합니다.

```php
$articles = Article::query()
    ->whereFullText('body', $request->input('query'))
    ->limit(50)
    ->get()
    ->rerank('body', $request->input('query'), limit: 10);
```

**벡터 검색 + 전통적 필터(Vector Search + Traditional Filters)**

벡터 유사도 기반 검색과 일반적인 `where` 조건을 결합해, 의미 중심 검색을 하면서도 소유권, 카테고리 등의 속성으로 결과를 제한할 수 있습니다.

```php
$documents = Document::query()
    ->where('team_id', $user->team_id)
    ->whereVectorSimilarTo('embedding', $request->input('query'))
    ->limit(10)
    ->get();
```