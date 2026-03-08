# Laravel Scout

- [소개](#introduction)
- [설치](#installation)
    - [큐 사용](#queueing)
- [드라이버 사전 요구 사항](#driver-prerequisites)
- [설정](#configuration)
    - [검색 가능한 데이터 설정](#configuring-searchable-data)
- [Database / Collection 엔진](#database-and-collection-engines)
    - [Database 엔진](#database-engine)
    - [Collection 엔진](#collection-engine)
- [서드파티 엔진 설정](#third-party-engine-configuration)
    - [모델 인덱스 설정](#configuring-model-indexes)
    - [Algolia](#algolia-configuration)
    - [Meilisearch](#meilisearch-configuration)
    - [Typesense](#typesense-configuration)
- [서드파티 엔진 인덱싱](#indexing)
    - [일괄 가져오기](#batch-import)
    - [레코드 추가](#adding-records)
    - [레코드 업데이트](#updating-records)
    - [레코드 제거](#removing-records)
    - [인덱싱 일시 중지](#pausing-indexing)
    - [조건부 검색 가능 모델 인스턴스](#conditionally-searchable-model-instances)
- [검색](#searching)
    - [Where 절](#where-clauses)
    - [페이지네이션](#pagination)
    - [Soft Delete](#soft-deleting)
    - [엔진 검색 사용자 정의](#customizing-engine-searches)
- [커스텀 엔진](#custom-engines)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Scout](https://github.com/laravel/scout)는 [Eloquent 모델](/docs/master/eloquent)에 **풀텍스트 검색(full-text search)** 기능을 추가할 수 있도록 간단한 드라이버 기반 솔루션을 제공합니다. Scout는 모델 옵저버(model observer)를 사용하여 Eloquent 레코드와 검색 인덱스가 자동으로 동기화되도록 관리합니다.

Scout는 기본적으로 `database` 엔진을 제공합니다. 이 엔진은 MySQL / PostgreSQL의 **full-text 인덱스**와 `LIKE` 절을 사용하여 기존 데이터베이스를 검색합니다. 별도의 외부 서비스가 필요하지 않습니다. 대부분의 애플리케이션에서는 이 방식만으로도 충분합니다. Laravel에서 제공되는 모든 검색 옵션에 대한 개요는 [검색 문서](/docs/master/search)를 참고하시기 바랍니다.

또한 Scout는 대규모 환경에서 **오타 허용 검색(typo tolerance)**, **패싯 필터링(faceted filtering)**, **지리 기반 검색(geo-search)** 같은 기능이 필요한 경우를 위해 [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), [Typesense](https://typesense.org) 드라이버도 제공합니다.  

로컬 개발 환경을 위한 `"collection"` 드라이버도 제공되며, 필요하다면 직접 [커스텀 엔진](#custom-engines)을 작성할 수도 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 매니저를 사용하여 Scout를 설치합니다.

```shell
composer require laravel/scout
```

Scout 설치 후 `vendor:publish` Artisan 명령어를 사용하여 Scout 설정 파일을 게시합니다. 이 명령어는 `scout.php` 설정 파일을 애플리케이션의 `config` 디렉토리에 생성합니다.

```shell
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

마지막으로 검색 기능을 사용할 모델에 `Laravel\Scout\Searchable` trait을 추가합니다. 이 trait은 모델 옵저버를 등록하여 모델 데이터와 검색 드라이버의 인덱스를 자동으로 동기화합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;
}
```

<a name="queueing"></a>
### 큐 사용

`database` 또는 `collection` 엔진이 아닌 다른 엔진을 사용할 경우, 라이브러리를 사용하기 전에 [queue driver](/docs/master/queues)를 설정하는 것을 강력히 권장합니다.

큐 워커(queue worker)를 실행하면 Scout가 모델 정보를 검색 인덱스와 동기화하는 작업을 **큐에 등록하여 비동기적으로 처리**할 수 있습니다. 이를 통해 웹 인터페이스의 응답 속도를 크게 향상시킬 수 있습니다.

큐 드라이버 설정 후 `config/scout.php` 파일에서 `queue` 옵션을 `true`로 설정합니다.

```php
'queue' => true,
```

`queue` 옵션이 `false`여도 Algolia나 Meilisearch 같은 일부 Scout 드라이버는 항상 **비동기 방식으로 인덱싱**을 수행합니다. 즉 Laravel 애플리케이션에서는 인덱싱 작업이 완료되었더라도 실제 검색 엔진에는 즉시 반영되지 않을 수 있습니다.

Scout 작업이 사용할 connection과 queue를 지정하려면 다음과 같이 설정할 수 있습니다.

```php
'queue' => [
    'connection' => 'redis',
    'queue' => 'scout'
],
```

이 경우 해당 connection과 queue에서 작업을 처리하도록 큐 워커를 실행해야 합니다.

```shell
php artisan queue:work redis --queue=scout
```

<a name="driver-prerequisites"></a>
## 드라이버 사전 요구 사항 (Driver Prerequisites)

<a name="algolia"></a>
### Algolia

Algolia 드라이버를 사용할 경우 `config/scout.php` 설정 파일에 Algolia `id`와 `secret` 인증 정보를 설정해야 합니다. 설정 후 Composer를 통해 Algolia PHP SDK를 설치합니다.

```shell
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
### Meilisearch

[Meilisearch](https://www.meilisearch.com)는 빠른 오픈소스 검색 엔진입니다. 로컬 환경에 설치하는 방법을 모르는 경우 Laravel의 공식 Docker 개발 환경인 [Laravel Sail](/docs/master/sail#meilisearch)을 사용할 수 있습니다.

Meilisearch 드라이버를 사용할 경우 Composer를 통해 Meilisearch PHP SDK를 설치합니다.

```shell
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

그 다음 `.env` 파일에 다음 환경 변수를 설정합니다.

```ini
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

자세한 내용은 [Meilisearch 문서](https://docs.meilisearch.com/learn/getting_started/quick_start.html)를 참고하십시오.

또한 `meilisearch/meilisearch-php` 패키지 버전이 설치된 Meilisearch 바이너리 버전과 호환되는지 확인해야 합니다. 자세한 내용은 [Meilisearch 호환성 문서](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)를 참고하십시오.

> [!WARNING]
> Meilisearch를 사용하는 애플리케이션에서 Scout를 업그레이드할 때는 반드시 [Meilisearch 릴리스 노트](https://github.com/meilisearch/Meilisearch/releases)의 **Breaking Changes**를 확인해야 합니다.

<a name="typesense"></a>
### Typesense

[Typesense](https://typesense.org)는 매우 빠른 오픈소스 검색 엔진이며 다음 기능을 지원합니다.

- 키워드 검색
- 시맨틱 검색
- 지리 기반 검색
- 벡터 검색

Typesense는 직접 호스팅([self-host](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting))하거나 [Typesense Cloud](https://cloud.typesense.org)를 사용할 수 있습니다.

Scout에서 Typesense를 사용하려면 Composer를 통해 Typesense PHP SDK를 설치합니다.

```shell
composer require typesense/typesense-php
```

그 다음 `.env` 파일에 다음 환경 변수를 설정합니다.

```ini
SCOUT_DRIVER=typesense
TYPESENSE_API_KEY=masterKey
TYPESENSE_HOST=localhost
```

[Laravel Sail](/docs/master/sail)을 사용하는 경우 `TYPESENSE_HOST` 값을 Docker 컨테이너 이름에 맞게 수정해야 할 수 있습니다. 또한 다음 옵션을 추가로 설정할 수 있습니다.

```ini
TYPESENSE_PORT=8108
TYPESENSE_PATH=
TYPESENSE_PROTOCOL=http
```

Typesense 컬렉션의 추가 설정과 스키마 정의는 `config/scout.php` 설정 파일에서 확인할 수 있습니다. 자세한 내용은 [Typesense 문서](https://typesense.org/docs/guide/#quick-start)를 참고하십시오.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="configuring-searchable-data"></a>
### 검색 가능한 데이터 설정

기본적으로 모델의 `toArray` 결과 전체가 검색 인덱스에 저장됩니다.

검색 인덱스에 동기화되는 데이터를 직접 정의하려면 모델에서 `toSearchableArray` 메서드를 오버라이드하면 됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * Get the indexable data array for the model.
     *
     * @return array<string, mixed>
     */
    public function toSearchableArray(): array
    {
        $array = $this->toArray();

        // Customize the data array...

        return $array;
    }
}
```

<a name="configuring-search-engines-per-model"></a>
#### 모델별 검색 엔진 설정

일반적으로 Scout는 `scout` 설정 파일에 지정된 기본 검색 엔진을 사용합니다. 하지만 특정 모델에서 다른 검색 엔진을 사용하도록 설정할 수도 있습니다.

이를 위해 모델에서 `searchableUsing` 메서드를 오버라이드합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Engines\Engine;
use Laravel\Scout\Scout;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * Get the engine used to index the model.
     */
    public function searchableUsing(): Engine
    {
        return Scout::engine('meilisearch');
    }
}
```

<a name="database-and-collection-engines"></a>
## Database / Collection 엔진 (Database / Collection Engines)

<a name="database-engine"></a>
### Database 엔진

> [!WARNING]
> 현재 database 엔진은 MySQL과 PostgreSQL만 지원하며, 두 데이터베이스 모두 빠른 **full-text 컬럼 인덱싱**을 지원합니다.

`database` 엔진은 MySQL / PostgreSQL의 **full-text 인덱스**와 `LIKE` 절을 사용하여 데이터베이스를 직접 검색합니다.

많은 애플리케이션에서 이 방법이 가장 단순하고 실용적인 검색 구현 방식입니다. 별도의 외부 서비스나 추가 인프라가 필요하지 않습니다.

사용하려면 `.env` 파일에서 다음과 같이 설정합니다.

```ini
SCOUT_DRIVER=database
```

설정 후 [검색 데이터 정의](#configuring-searchable-data)를 하고 바로 [검색 쿼리 실행](#searching)을 시작할 수 있습니다.

서드파티 엔진과 달리 database 엔진은 **별도의 인덱싱 과정이 필요 없습니다.** 데이터베이스 테이블을 직접 검색합니다.

#### Database 검색 전략 커스터마이징

기본적으로 database 엔진은 검색 가능한 모든 모델 속성에 대해 `LIKE` 쿼리를 실행합니다.

하지만 특정 컬럼에 대해 더 효율적인 검색 전략을 지정할 수 있습니다.

- `SearchUsingFullText` → 데이터베이스 **full-text index** 사용
- `SearchUsingPrefix` → 문자열 **접두사(prefix)** 검색 (`example%`)

속성이 지정되지 않은 컬럼은 기본 `LIKE` 전략을 사용합니다.

```php
use Laravel\Scout\Attributes\SearchUsingFullText;
use Laravel\Scout\Attributes\SearchUsingPrefix;

/**
 * Get the indexable data array for the model.
 *
 * @return array<string, mixed>
 */
#[SearchUsingPrefix(['id', 'email'])]
#[SearchUsingFullText(['bio'])]
public function toSearchableArray(): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'bio' => $this->bio,
    ];
}
```

> [!WARNING]
> `SearchUsingFullText`를 사용하려면 해당 컬럼에 [full text index](/docs/master/migrations#available-index-types)가 반드시 생성되어 있어야 합니다.

<a name="collection-engine"></a>
### Collection 엔진

`collection` 엔진은 다음과 같은 상황에서 사용하기 위한 엔진입니다.

- 빠른 프로토타입
- 매우 작은 데이터셋(수백 개 수준)
- 테스트 환경

이 엔진은 데이터베이스에서 **모든 레코드를 가져온 뒤**, Laravel의 `Str::is` 헬퍼를 사용해 PHP에서 필터링합니다.

따라서 인덱싱이나 데이터베이스 특화 기능이 필요하지 않습니다.

```ini
SCOUT_DRIVER=collection
```

하지만 이 방식은 효율성이 매우 낮기 때문에 실제 서비스 환경에서는 [database 엔진](#database-engine) 사용을 권장합니다.

#### Database 엔진과의 차이점

- **Database 엔진**
  - full-text index 및 `LIKE` 사용
  - 효율적
  - 대규모 데이터에 적합

- **Collection 엔진**
  - 모든 레코드를 가져와 PHP에서 필터링
  - 모든 Laravel 지원 DB에서 동작
  - 성능이 매우 낮음

<a name="third-party-engine-configuration"></a>
## 서드파티 엔진 설정 (Third-Party Engine Configuration)

이 섹션의 설정은 **Algolia, Meilisearch, Typesense** 같은 서드파티 검색 엔진을 사용할 때만 적용됩니다.

[database 엔진](#database-engine)을 사용하는 경우 이 섹션은 건너뛰어도 됩니다.

<a name="configuring-model-indexes"></a>
### 모델 인덱스 설정

서드파티 엔진을 사용할 경우 각 Eloquent 모델은 **검색 인덱스(index)**와 동기화됩니다.

기본적으로 인덱스 이름은 모델의 **테이블 이름**과 동일합니다.

예:  
`Post` → `posts`

필요하다면 `searchableAs` 메서드를 오버라이드하여 인덱스 이름을 변경할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * Get the name of the index associated with the model.
     */
    public function searchableAs(): string
    {
        return 'posts_index';
    }
}
```

> [!NOTE]
> `searchableAs` 메서드는 database 엔진에서는 동작하지 않습니다.

<a name="configuring-the-model-id"></a>
#### 모델 ID 설정

기본적으로 Scout는 모델의 **primary key**를 검색 인덱스의 고유 ID로 사용합니다.

이를 변경하려면 `getScoutKey`와 `getScoutKeyName` 메서드를 오버라이드합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * Get the value used to index the model.
     */
    public function getScoutKey(): mixed
    {
        return $this->email;
    }

    /**
     * Get the key name used to index the model.
     */
    public function getScoutKeyName(): mixed
    {
        return 'email';
    }
}
```

> [!NOTE]
> database 엔진에서는 항상 모델의 primary key를 사용합니다.

(이후 섹션들도 동일한 방식으로 계속 번역됩니다.)