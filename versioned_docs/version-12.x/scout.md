# Laravel Scout (Laravel Scout)

- [소개](#introduction)
- [설치](#installation)
    - [큐(queue) 사용](#queueing)
- [드라이버 사전 준비 사항](#driver-prerequisites)
- [설정](#configuration)
    - [검색 대상 데이터 설정](#configuring-searchable-data)
- [데이터베이스 / 컬렉션 엔진](#database-and-collection-engines)
    - [데이터베이스 엔진](#database-engine)
    - [컬렉션 엔진](#collection-engine)
- [서드파티 엔진 설정](#third-party-engine-configuration)
    - [모델 인덱스 설정](#configuring-model-indexes)
    - [Algolia](#algolia-configuration)
    - [Meilisearch](#meilisearch-configuration)
    - [Typesense](#typesense-configuration)
- [서드파티 엔진 인덱싱](#indexing)
    - [배치 임포트](#batch-import)
    - [레코드 추가](#adding-records)
    - [레코드 업데이트](#updating-records)
    - [레코드 삭제](#removing-records)
    - [인덱싱 일시 중지](#pausing-indexing)
    - [조건부 검색 가능 모델 인스턴스](#conditionally-searchable-model-instances)
- [검색](#searching)
    - [Where 절](#where-clauses)
    - [페이지네이션](#pagination)
    - [소프트 삭제](#soft-deleting)
    - [엔진 검색 커스터마이즈](#customizing-engine-searches)
- [커스텀 엔진](#custom-engines)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Scout](https://github.com/laravel/scout)는 [Eloquent 모델](/docs/12.x/eloquent)에 전체 텍스트 검색 기능을 간단하고 드라이버 기반으로 추가할 수 있는 솔루션을 제공합니다. Scout는 모델 옵저버를 활용하여 Eloquent 레코드와 검색 인덱스를 자동으로 동기화합니다.

Scout는 별도의 외부 서비스 없이 MySQL / PostgreSQL의 전체 텍스트 인덱스와 `LIKE` 절을 활용하는 내장 `database` 엔진을 기본 제공합니다. 대부분의 애플리케이션에서는 이 방식만으로도 충분합니다. Laravel에서 제공하는 다양한 검색 옵션의 개요는 [검색 문서](/docs/12.x/search)를 참고하시기 바랍니다.

또한 대규모 오타 허용, 페이시티드 필터링, 지리 검색과 같은 기능이 필요한 경우 [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), [Typesense](https://typesense.org) 드라이버도 지원합니다. 로컬 개발 환경을 위한 "컬렉션" 드라이버 역시 제공되며, 필요에 따라 [커스텀 엔진](#custom-engines)도 직접 작성할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저, Composer 패키지 매니저를 통해 Scout를 설치합니다:

```shell
composer require laravel/scout
```

Scout를 설치한 후, `vendor:publish` Artisan 명령어를 사용하여 Scout 설정 파일을 퍼블리시해야 합니다. 이 명령어는 `scout.php` 설정 파일을 애플리케이션의 `config` 디렉터리에 복사합니다:

```shell
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

마지막으로, 검색 가능하게 만들고자 하는 모델에 `Laravel\Scout\Searchable` 트레이트를 추가합니다. 이 트레이트는 모델 옵저버를 등록하여 해당 모델이 검색 드라이버와 자동으로 동기화되도록 해줍니다:

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
### 큐(queue) 사용

`database`나 `collection` 엔진이 아닌 다른 엔진을 사용할 경우, 라이브러리를 사용하기 전에 [큐 드라이버](/docs/12.x/queues)를 반드시 설정하는 것이 좋습니다. 큐 워커를 실행하면 모델 정보를 검색 인덱스와 동기화하는 모든 작업을 큐로 처리하여, 애플리케이션 웹 인터페이스의 응답 속도를 대폭 향상시킬 수 있습니다.

큐 드라이버를 설정한 후에는 `config/scout.php` 설정 파일에서 `queue` 옵션 값을 `true`로 지정합니다:

```php
'queue' => true,
```

`queue` 옵션이 `false`로 설정되어 있더라도, Algolia나 Meilisearch 등 일부 Scout 드라이버는 항상 비동기적으로 인덱싱을 수행한다는 점을 유의해야 합니다. 즉, 인덱싱 작업이 Laravel 애플리케이션 내에서는 완료 표시가 되어도, 검색 엔진에서는 새로운 또는 수정된 레코드가 즉시 반영되지 않을 수 있습니다.

Scout 작업에 사용할 커넥션과 큐를 지정하려면, 배열 형태로 `queue` 설정을 정의할 수 있습니다:

```php
'queue' => [
    'connection' => 'redis',
    'queue' => 'scout'
],
```

커스텀 커넥션과 큐를 지정했다면, 해당 커넥션과 큐에서 작업을 처리할 큐 워커를 실행해야 합니다:

```shell
php artisan queue:work redis --queue=scout
```

<a name="driver-prerequisites"></a>
## 드라이버 사전 준비 사항 (Driver Prerequisites)

<a name="algolia"></a>
### Algolia

Algolia 드라이버를 사용할 때는, Algolia `id`와 `secret` 인증 정보를 `config/scout.php` 파일에 지정해야 합니다. 인증 정보 설정을 마쳤다면 Composer 패키지 매니저로 Algolia PHP SDK도 설치해야 합니다:

```shell
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
### Meilisearch

[Meilisearch](https://www.meilisearch.com)는 빠르고 오픈 소스인 검색 엔진입니다. 로컬 환경에서 Meilisearch 설치 방법을 잘 모를 경우, Laravel의 공식 Docker 개발 환경인 [Laravel Sail](/docs/12.x/sail#meilisearch)을 활용할 수 있습니다.

Meilisearch 드라이버 사용 시에는 Composer 패키지 매니저로 Meilisearch PHP SDK를 설치해야 합니다:

```shell
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

그리고, `.env` 파일에 `SCOUT_DRIVER` 환경 변수와 Meilisearch의 `host`, `key` 값을 다음과 같이 지정합니다:

```ini
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

Meilisearch에 관한 자세한 내용은 [Meilisearch 공식 문서](https://docs.meilisearch.com/learn/getting_started/quick_start.html)를 참고하시기 바랍니다.

또한, `meilisearch/meilisearch-php` 패키지의 버전이 Meilisearch 바이너리 버전과 호환되는지 반드시 [Meilisearch 바이너리 호환성 문서](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)를 참고하여 확인해야 합니다.

> [!WARNING]
> Meilisearch를 사용하는 애플리케이션에서 Scout를 업그레이드할 때에는 항상 Meilisearch 서비스 자체의 [추가적인 브레이킹 체인지](https://github.com/meilisearch/Meilisearch/releases)가 있는지 확인해야 합니다.

<a name="typesense"></a>
### Typesense

[Typesense](https://typesense.org)는 매우 빠른 오픈 소스 검색 엔진으로, 키워드 검색, 의미론적 검색, 지리 기반 검색, 벡터 검색을 지원합니다.

Typesense는 [자가 호스팅](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting)하거나 [Typesense Cloud](https://cloud.typesense.org)를 사용할 수 있습니다.

Scout에서 Typesense를 사용하려면, Composer 패키지 매니저로 Typesense PHP SDK를 설치해야 합니다:

```shell
composer require typesense/typesense-php
```

그 다음, `.env` 파일에 `SCOUT_DRIVER` 환경 변수와 Typesense의 host, API key 값을 지정합니다:

```ini
SCOUT_DRIVER=typesense
TYPESENSE_API_KEY=masterKey
TYPESENSE_HOST=localhost
```

[Laravel Sail](/docs/12.x/sail)을 사용하는 경우, `TYPESENSE_HOST` 값을 Docker 컨테이너 이름에 맞게 조정해야 할 수도 있습니다. 또한, 설치 환경의 포트, 경로, 프로토콜도 선택적으로 지정할 수 있습니다:

```ini
TYPESENSE_PORT=8108
TYPESENSE_PATH=
TYPESENSE_PROTOCOL=http
```

Typesense 컬렉션의 추가 설정 및 스키마 정의는 `config/scout.php`에서 가능합니다. Typesense에 대한 자세한 정보는 [Typesense 공식 문서](https://typesense.org/docs/guide/#quick-start)를 참고하세요.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="configuring-searchable-data"></a>
### 검색 대상 데이터 설정

기본적으로, 모델의 `toArray` 결과 전체가 해당 모델의 검색 인덱스에 저장됩니다. 동기화할 데이터를 커스터마이즈하려면, 모델에서 `toSearchableArray` 메서드를 오버라이딩하여 원하는 데이터를 리턴하도록 설정할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * 모델의 인덱싱 대상 데이터 배열 반환
     *
     * @return array<string, mixed>
     */
    public function toSearchableArray(): array
    {
        $array = $this->toArray();

        // 데이터 배열 커스터마이즈...

        return $array;
    }
}
```

<a name="configuring-search-engines-per-model"></a>
#### 모델 별 엔진 설정

Scout는 기본적으로 애플리케이션의 `scout` 설정 파일에 지정된 기본 검색 엔진을 사용합니다. 단, 특정 모델에서 사용할 엔진을 변경하려면 해당 모델에서 `searchableUsing` 메서드를 오버라이딩하면 됩니다:

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
     * 이 모델에 사용할 엔진 반환
     */
    public function searchableUsing(): Engine
    {
        return Scout::engine('meilisearch');
    }
}
```

<a name="database-and-collection-engines"></a>
## 데이터베이스 / 컬렉션 엔진 (Database / Collection Engines)

<a name="database-engine"></a>
### 데이터베이스 엔진 (Database Engine)

> [!WARNING]
> 데이터베이스 엔진은 현재 MySQL과 PostgreSQL만 지원하며, 두 데이터베이스 모두 빠른 전체 텍스트 컬럼 인덱싱을 지원합니다.

`database` 엔진은 MySQL / PostgreSQL의 전체 텍스트 인덱스와 `LIKE` 절을 활용하여 기존 데이터베이스에서 직접 검색을 수행합니다. 별도의 외부 서비스나 인프라 없이 가장 간단하고 실용적으로 검색 기능을 추가할 수 있습니다.

데이터베이스 엔진을 사용하려면 `.env` 파일에서 `SCOUT_DRIVER` 환경 변수 값을 `database`로 지정합니다:

```ini
SCOUT_DRIVER=database
```

설정이 완료되면, [검색 대상 데이터](#configuring-searchable-data)를 정의하고 모델에 대해 [검색 쿼리](#searching)를 실행할 수 있습니다. 서드파티 엔진과 달리, 데이터베이스 엔진은 별도의 인덱싱 단계 없이 데이터베이스 테이블을 직접 검색합니다.

#### 데이터베이스 검색 방식 커스터마이즈

기본적으로 데이터베이스 엔진은 [검색 대상 데이터](#configuring-searchable-data)로 지정한 모든 속성에 대해 `LIKE` 쿼리를 실행합니다. 그러나 특정 컬럼에 더 효율적인 검색 전략을 지정할 수도 있습니다. `SearchUsingFullText` 속성은 해당 컬럼에 전체 텍스트 인덱스를 활용하고, `SearchUsingPrefix`는 문자열의 시작 부분(`example%`)만을 대상으로 검색합니다(`%example%`와는 다름).

이 기능을 활용하려면, 모델의 `toSearchableArray` 메서드에 PHP 속성을 지정하면 됩니다. 속성이 지정되지 않은 컬럼은 기본 `LIKE` 검색이 적용됩니다:

```php
use Laravel\Scout\Attributes\SearchUsingFullText;
use Laravel\Scout\Attributes\SearchUsingPrefix;

/**
 * 모델의 인덱싱 대상 데이터 배열 반환
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
> 컬럼에 전체 텍스트 쿼리를 적용하려면, 해당 컬럼에 [전체 텍스트 인덱스](/docs/12.x/migrations#available-index-types)가 생성되어 있어야 합니다.

<a name="collection-engine"></a>
### 컬렉션 엔진 (Collection Engine)

"컬렉션" 엔진은 빠른 프로토타입 제작, 아주 작은 데이터셋(수백 건 이하), 테스트 실행 목적에 적합합니다. 컬렉션 엔진은 데이터베이스에서 모든 레코드를 불러와, Laravel의 `Str::is` 헬퍼를 이용해 PHP에서 필터링하므로 별도의 인덱싱이나 데이터베이스 특화 기능이 필요 없습니다. 그 외의 경우에는 [데이터베이스 엔진](#database-engine) 사용이 권장됩니다.

컬렉션 엔진을 사용하려면, `.env` 파일에서 `SCOUT_DRIVER` 값을 `collection`으로 설정하거나, `scout` 설정 파일에 드라이버 값을 직접 지정하면 됩니다:

```ini
SCOUT_DRIVER=collection
```

컬렉션 드라이버를 지정하면, 모델에 대해 즉시 [검색 쿼리](#searching)를 실행할 수 있습니다. Algolia, Meilisearch, Typesense 등 별도의 인덱스 생성을 필요로 하는 엔진과 달리, 컬렉션 엔진은 인덱스 작업이 필요 없습니다.

#### 데이터베이스 엔진과의 차이점

데이터베이스 엔진이 전체 텍스트 인덱스와 `LIKE` 절을 활용해 검색을 효율적으로 수행하는 반면, 컬렉션 엔진은 모든 레코드를 불러와 PHP에서 필터링합니다. 컬렉션 엔진은 Laravel이 지원하는 모든 관계형 데이터베이스(SQLite, SQL Server 포함)에서 동작하므로 이식성은 높지만, 대량 데이터셋에는 부적합하며 성능이 매우 떨어집니다.

<a name="third-party-engine-configuration"></a>
## 서드파티 엔진 설정 (Third-Party Engine Configuration)

아래 설정 옵션들은 Algolia, Meilisearch, Typesense와 같이 서드파티 검색 엔진을 사용할 때에만 적용됩니다. [데이터베이스 엔진](#database-engine)을 사용하는 경우 이 절은 건너뛰어도 됩니다.

<a name="configuring-model-indexes"></a>
### 모델 인덱스 설정

서드파티 엔진 사용 시 각 Eloquent 모델은 하나의 검색 "인덱스"와 동기화되며, 해당 인덱스에는 모델의 모든 검색 대상 레코드가 저장됩니다. 기본적으로 각 모델은 모델의 일반적인 "테이블" 이름과 일치하는 인덱스에 저장됩니다(일반적으로 모델 이름의 복수형). 하지만, `searchableAs` 메서드를 오버라이딩하여 인덱스 이름을 자유롭게 지정할 수도 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * 모델과 연결된 인덱스 이름 반환
     */
    public function searchableAs(): string
    {
        return 'posts_index';
    }
}
```

> [!NOTE]
> `searchableAs` 메서드는 데이터베이스 엔진에서는 아무런 효과가 없습니다. 데이터베이스 엔진은 항상 모델의 테이블을 직접 검색합니다.

<a name="configuring-the-model-id"></a>
#### 모델 ID 설정

기본적으로 Scout는 모델의 기본 키(primary key)를 인덱스의 유니크 ID로 사용합니다. 서드파티 엔진에서 이 동작을 변경해야 할 경우, 모델에서 `getScoutKey`와 `getScoutKeyName` 메서드를 오버라이딩하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * 인덱스에 사용할 값 반환
     */
    public function getScoutKey(): mixed
    {
        return $this->email;
    }

    /**
     * 인덱스에 사용할 키 이름 반환
     */
    public function getScoutKeyName(): mixed
    {
        return 'email';
    }
}
```

> [!NOTE]
> `getScoutKey`와 `getScoutKeyName` 메서드는 데이터베이스 엔진에서는 아무런 효과가 없습니다. 데이터베이스 엔진은 항상 모델의 기본 키를 사용합니다.

<a name="algolia-configuration"></a>
### Algolia

<a name="algolia-index-settings"></a>
#### 인덱스 설정

Algolia 인덱스에 추가 설정이 필요할 때도 있습니다. Algolia UI를 통해 설정할 수도 있지만, 자동 배포 파이프라인에서 일관된 환경을 유지하기 위해 애플리케이션의 `config/scout.php` 설정 파일에서 인덱스 상태를 관리하는 방식이 더 효율적일 수 있습니다.

이런 방식으로 필터 속성, 정렬 방식, 페이시팅 또는 [기타 지원되는 모든 설정](https://www.algolia.com/doc/rest-api/search/#tag/Indices/operation/setSettings)을 지정할 수 있습니다.

우선 애플리케이션의 `config/scout.php`에 각 인덱스별 설정을 추가합니다:

```php
use App\Models\User;
use App\Models\Flight;

'algolia' => [
    'id' => env('ALGOLIA_APP_ID', ''),
    'secret' => env('ALGOLIA_SECRET', ''),
    'index-settings' => [
        User::class => [
            'searchableAttributes' => ['id', 'name', 'email'],
            'attributesForFaceting'=> ['filterOnly(email)'],
            // 기타 설정 필드...
        ],
        Flight::class => [
            'searchableAttributes'=> ['id', 'destination'],
        ],
    ],
],
```

특정 인덱스 모델이 소프트 삭제를 지원하고 `index-settings` 배열에 포함된 경우, Scout는 해당 인덱스에 소프트 삭제 모델을 위한 패시팅도 자동 지원합니다. 소프트 삭제 외에 다른 페이시팅 속성이 필요 없다면, 모델에 대해 빈 엔트리를 추가해도 됩니다:

```php
'index-settings' => [
    Flight::class => []
],
```

설정을 완료한 후에는 `scout:sync-index-settings` Artisan 명령어를 실행해야 합니다. 이 명령어가 Algolia에 현재의 인덱스 설정 정보를 동기화합니다. 이 과정을 배포 프로세스의 일부로 지정해두는 것이 좋습니다:

```shell
php artisan scout:sync-index-settings
```

<a name="algolia-identifying-users"></a>
#### 사용자 식별

Scout는 Algolia 사용 시 사용자 자동 식별 기능을 제공합니다. 인증된 사용자와 검색 작업을 연동하여 Algolia의 대시보드에서 검색 분석을 확인할 수 있습니다. 이 기능은 `.env` 파일에서 `SCOUT_IDENTIFY` 환경 변수를 `true`로 설정하면 활성화됩니다:

```ini
SCOUT_IDENTIFY=true
```

이 설정이 활성화되면, 현재 요청의 IP 주소와 인증된 사용자 기본 식별자가 Algolia로 전송되어 검색 요청과 함께 기록됩니다.

<a name="meilisearch-configuration"></a>
### Meilisearch

<a name="meilisearch-index-settings"></a>
#### 인덱스 설정

Meilisearch는 필터링 속성, 정렬 가능 속성 등을 비롯한 [여러 검색 설정 필드](https://docs.meilisearch.com/reference/api/settings.html)를 사전에 정의해야 합니다.

필터 속성은 Scout의 `where` 메서드로 필터링에 활용할 속성이며, 정렬 가능 속성은 `orderBy` 메서드로 정렬할 속성입니다. 인덱스 설정은 `scout` 설정 파일의 `meilisearch` 엔트리 아래 `index-settings` 항목에서 지정합니다:

```php
use App\Models\User;
use App\Models\Flight;

'meilisearch' => [
    'host' => env('MEILISEARCH_HOST', 'http://localhost:7700'),
    'key' => env('MEILISEARCH_KEY', null),
    'index-settings' => [
        User::class => [
            'filterableAttributes'=> ['id', 'name', 'email'],
            'sortableAttributes' => ['created_at'],
            // 기타 설정 필드...
        ],
        Flight::class => [
            'filterableAttributes'=> ['id', 'destination'],
            'sortableAttributes' => ['updated_at'],
        ],
    ],
],
```

특정 인덱스의 모델이 소프트 삭제 기능을 지원하고 `index-settings`에 포함된 경우, Scout는 해당 인덱스에 대해서 소프트 삭제 모델 필터링도 자동으로 지원합니다. 필터, 정렬 속성이 없는 경우에는 빈 엔트리를 추가하면 됩니다:

```php
'index-settings' => [
    Flight::class => []
],
```

설정을 마치고 나면, `scout:sync-index-settings` Artisan 명령어를 실행해야 하며, 이 과정도 배포 과정에서 자동 실행하도록 포함하는 것이 좋습니다:

```shell
php artisan scout:sync-index-settings
```

<a name="meilisearch-data-types"></a>
#### 검색 데이터 타입

Meilisearch에서 필터(>, < 등) 연산을 제대로 수행하려면 데이터의 타입이 정확해야 합니다. `toSearchableArray`를 커스터마이즈할 때에는 숫자 값이 적절한 타입으로 캐스팅되어야 합니다:

```php
public function toSearchableArray()
{
    return [
        'id' => (int) $this->id,
        'name' => $this->name,
        'price' => (float) $this->price,
    ];
}
```

<a name="typesense-configuration"></a>
### Typesense

<a name="typesense-searchable-data"></a>
#### 검색 대상 데이터 준비

Typesense를 사용할 때, 검색 대상 모델에는 반드시 `id`(기본 키)를 문자열로, 생성일을 UNIX timestamp로 변환하는 `toSearchableArray` 메서드를 정의해야 합니다:

```php
/**
 * 모델의 인덱싱 대상 데이터 배열 반환
 *
 * @return array<string, mixed>
 */
public function toSearchableArray(): array
{
    return array_merge($this->toArray(),[
        'id' => (string) $this->id,
        'created_at' => $this->created_at->timestamp,
    ]);
}
```

Typesense 컬렉션 스키마는 `config/scout.php` 파일에서 정의할 수 있습니다. 컬렉션 스키마는 Typesense에서 검색 가능한 각 필드의 데이터 타입을 지정합니다. 사용 가능한 스키마 옵션에 대한 자세한 정보는 [Typesense 공식 문서](https://typesense.org/docs/latest/api/collections.html#schema-parameters)를 참고하세요.

기존에 정의된 스키마를 변경하려면 `scout:flush`와 `scout:import`를 실행하여 모든 인덱스 데이터를 삭제하고 스키마를 재생성하거나, Typesense API를 이용하여 컬렉션의 스키마만 수정할 수도 있습니다.

검색 대상 모델이 소프트 삭제를 지원한다면, 모델에 해당하는 Typesense 컬렉션 스키마에 `__soft_deleted` 필드를 추가해야 합니다:

```php
User::class => [
    'collection-schema' => [
        'fields' => [
            // ...
            [
                'name' => '__soft_deleted',
                'type' => 'int32',
                'optional' => true,
            ],
        ],
    ],
],
```

<a name="typesense-dynamic-search-parameters"></a>
#### 동적 검색 파라미터

Typesense는 [검색 파라미터](https://typesense.org/docs/latest/api/search.html#search-parameters)를 검색 시점에 `options` 메서드로 동적으로 지정할 수 있습니다:

```php
use App\Models\Todo;

Todo::search('Groceries')->options([
    'query_by' => 'title, description'
])->get();
```

<a name="indexing"></a>
## 서드파티 엔진 인덱싱 (Third-Party Engine Indexing)

> [!NOTE]
> 이하 인덱싱 기능은 주로 Algolia, Meilisearch, Typesense와 같은 서드파티 엔진 사용 시에 적용됩니다. 데이터베이스 엔진은 테이블에서 곧바로 검색하므로 별도 인덱스 관리가 필요 없습니다.

<a name="batch-import"></a>
### 배치 임포트 (Batch Import)

이미 데이터베이스에 존재하는 레코드를 인덱스에 임포트하려면, `scout:import` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan scout:import "App\Models\Post"
```

또는, [큐 작업](/docs/12.x/queues)으로 배치 임포트를 진행하려면 `scout:queue-import` 명령어를 사용할 수 있으며, `--chunk=500` 옵션 등으로 한 번에 처리할 레코드 수를 지정할 수 있습니다:

```shell
php artisan scout:queue-import "App\Models\Post" --chunk=500
```

모델의 모든 레코드를 인덱스에서 삭제하려면 `flush` 명령어를 사용합니다:

```shell
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
#### 임포트 쿼리 커스터마이즈

배치 임포트에서 가져올 모델 쿼리를 커스터마이즈하려면, 모델에 `makeAllSearchableUsing` 메서드를 정의합니다. 이 메서드는 모델을 임포트하기 전에 관계 미리 로딩 등 필요한 처리를 할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

/**
 * 모든 모델을 검색 가능하게 만들 때 사용하는 쿼리 커스터마이즈
 */
protected function makeAllSearchableUsing(Builder $query): Builder
{
    return $query->with('author');
}
```

> [!WARNING]
> 큐를 사용하여 배치 임포트할 때는 `makeAllSearchableUsing` 메서드가 적용되지 않을 수 있습니다. 큐 작업 처리 중에는 [관계가 복원되지 않습니다](/docs/12.x/queues#handling-relationships).

<a name="adding-records"></a>
### 레코드 추가 (Adding Records)

모델에 `Laravel\Scout\Searchable` 트레이트를 추가한 후에는, 모델 인스턴스를 `save` 또는 `create`만 하면 자동으로 검색 인덱스에 추가됩니다. Scout에서 [큐 사용](#queueing) 설정이 되어 있다면, 이 작업은 백그라운드 큐로 처리됩니다:

```php
use App\Models\Order;

$order = new Order;

// ...

$order->save();
```

<a name="adding-records-via-query"></a>
#### 쿼리를 통한 레코드 추가

Eloquent 쿼리 결과로 가져온 모델 컬렉션을 검색 인덱스에 추가하려면, 쿼리 뒤에 `searchable` 메서드를 체이닝합니다. 이 메서드는 [쿼리 결과를 청크 단위로 분할](/docs/12.x/eloquent#chunking-results)하여 인덱스에 추가합니다. 큐 설정이 되어 있다면, 청크 전체가 큐 워커에 의해 백그라운드에서 처리됩니다:

```php
use App\Models\Order;

Order::where('price', '>', 100)->searchable();
```

Eloquent 관계 인스턴스에도 `searchable`을 사용할 수 있습니다:

```php
$user->orders()->searchable();
```

이미 메모리에 컬렉션이 있다면, 해당 컬렉션 인스턴스에 `searchable`을 호출하여 인덱스에 추가할 수도 있습니다:

```php
$orders->searchable();
```

> [!NOTE]
> `searchable` 메서드는 일종의 "upsert" 연산으로 간주할 수 있습니다. 즉, 이미 인덱스에 존재하는 레코드는 업데이트되고, 존재하지 않으면 새로 추가됩니다.

<a name="updating-records"></a>
### 레코드 업데이트 (Updating Records)

검색 가능한 모델을 업데이트하려면, 모델 속성을 수정한 뒤 `save`만 호출하면 자동으로 인덱스에도 반영됩니다:

```php
use App\Models\Order;

$order = Order::find(1);

// 주문 내용 수정...

$order->save();
```

또는, Eloquent 쿼리에 `searchable` 메서드를 사용해 여러 모델을 한 번에 업데이트할 수도 있습니다. 인덱스에 존재하지 않는 레코드는 새로 등록됩니다:

```php
Order::where('price', '>', 100)->searchable();
```

관계 인스턴스에서도 `searchable`을 호출할 수 있습니다:

```php
$user->orders()->searchable();
```

또는, 이미 메모리에 있는 컬렉션도 가능합니다:

```php
$orders->searchable();
```

<a name="modifying-records-before-importing"></a>
#### 인덱싱 전 레코드 커스터마이즈

인덱스에 추가하기 전에 컬렉션을 미리 준비해야 할 때도 있습니다. 예를 들어, 관계 데이터를 미리 로드해서 인덱스에 포함시키고 싶다면, 모델에 `makeSearchableUsing` 메서드를 정의하면 됩니다:

```php
use Illuminate\Database\Eloquent\Collection;

/**
 * 인덱싱 대상 모델 컬렉션 커스터마이즈
 */
public function makeSearchableUsing(Collection $models): Collection
{
    return $models->load('author');
}
```

<a name="conditionally-updating-the-search-index"></a>
#### 인덱스 업데이트 조건 제어

기본적으로 Scout는 어떤 속성이 수정됐는지에 상관없이 모델이 업데이트되면 곧바로 인덱스도 갱신합니다. 이 동작을 커스터마이즈하려면, 모델에 `searchIndexShouldBeUpdated` 메서드를 정의할 수 있습니다:

```php
/**
 * 인덱스 갱신 여부 결정
 */
public function searchIndexShouldBeUpdated(): bool
{
    return $this->wasRecentlyCreated || $this->wasChanged(['title', 'body']);
}
```

<a name="removing-records"></a>
### 레코드 삭제 (Removing Records)

인덱스에서 레코드를 삭제하려면 모델을 데이터베이스에서 삭제하면 됩니다. [소프트 삭제](/docs/12.x/eloquent#soft-deleting) 모델도 마찬가지로 처리됩니다:

```php
use App\Models\Order;

$order = Order::find(1);

$order->delete();
```

레코드 조회 없이 바로 삭제하려면, Eloquent 쿼리에서 `unsearchable` 메서드를 사용할 수 있습니다:

```php
Order::where('price', '>', 100)->unsearchable();
```

관계 인스턴스에서도 사용 가능합니다:

```php
$user->orders()->unsearchable();
```

이미 메모리에 있는 컬렉션에 대해서도 가능합니다:

```php
$orders->unsearchable();
```

모델의 모든 레코드를 인덱스에서 한 번에 삭제하려면, `removeAllFromSearch` 메서드를 사용합니다:

```php
Order::removeAllFromSearch();
```

<a name="pausing-indexing"></a>
### 인덱싱 일시 중지 (Pausing Indexing)

모델 데이터를 검색 인덱스와 동기화하지 않고 일련의 Eloquent 작업을 수행해야 하는 상황이 있을 수 있습니다. 이때는 `withoutSyncingToSearch` 메서드를 사용할 수 있습니다. 이 메서드는 하나의 클로저를 받아 즉시 실행하며, 클로저 내부에서 일어나는 모델 작업은 인덱스에 반영되지 않습니다:

```php
use App\Models\Order;

Order::withoutSyncingToSearch(function () {
    // 모델 작업 수행...
});
```

<a name="conditionally-searchable-model-instances"></a>
### 조건부 검색 가능 모델 인스턴스 (Conditionally Searchable Model Instances)

특정 조건에서만 모델을 검색 가능하게 만들고 싶을 때가 있습니다. 예를 들어, `App\Models\Post` 모델이 "draft"와 "published" 두 상태를 가질 수 있고, "published"인 경우에만 검색이 가능하게 하려면, 모델에 `shouldBeSearchable` 메서드를 정의하면 됩니다:

```php
/**
 * 모델이 검색 대상이 될지 여부 결정
 */
public function shouldBeSearchable(): bool
{
    return $this->isPublished();
}
```

`shouldBeSearchable` 메서드는 `save`, `create`, 쿼리, 또는 관계를 통한 조작 시에만 적용됩니다. 직접 `searchable` 메서드를 호출하여 모델이나 컬렉션을 강제로 검색 가능하게 만드는 경우에는 이 조건이 무시됩니다.

> [!WARNING]
> "database" 엔진을 사용하는 경우, `shouldBeSearchable`은 적용되지 않습니다. 데이터베이스 엔진에서는 모든 검색 데이터가 항상 데이터베이스에 저장되므로, 이와 유사한 동작이 필요하다면 [where 절](#where-clauses)을 사용하십시오.

<a name="searching"></a>
## 검색 (Searching)

모델에서 검색을 시작하려면 `search` 메서드를 사용할 수 있습니다. 이 메서드는 검색에 사용할 문자열을 하나 받아, 그 결과에 다시 `get` 메서드를 체이닝하여 해당 Eloquent 모델 컬렉션을 반환받을 수 있습니다:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->get();
```

Scout 검색 결과는 Eloquent 모델 컬렉션이므로, 라우트 또는 컨트롤러에서 바로 반환하면 자동으로 JSON으로 변환할 수 있습니다:

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/search', function (Request $request) {
    return Order::search($request->search)->get();
});
```

검색 결과가 Eloquent 모델로 변환되기 전의 원본 결과를 받고 싶다면 `raw` 메서드를 사용할 수 있습니다:

```php
$orders = Order::search('Star Trek')->raw();
```

<a name="custom-indexes"></a>
#### 커스텀 인덱스 검색

서드파티 엔진 사용 시에는 보통 [searchableAs](#configuring-model-indexes) 메서드에서 지정한 인덱스에서 검색하게 됩니다. 하지만 `within` 메서드로 검색 인덱스를 직접 지정하여 쿼리를 실행할 수도 있습니다:

```php
$orders = Order::search('Star Trek')
    ->within('tv_shows_popularity_desc')
    ->get();
```

<a name="where-clauses"></a>
### Where 절

Scout는 검색 쿼리에 간단한 "where" 절을 추가할 수 있습니다. 현재는 기본적인 동등 비교만 지원하며, 주로 소유자 ID 등으로 검색 쿼리를 범위 제한하는 데 유용합니다:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->where('user_id', 1)->get();
```

또한 `whereIn` 메서드를 사용하면 지정한 컬럼의 값이 배열 내에 포함되어 있는지 확인할 수 있습니다:

```php
$orders = Order::search('Star Trek')->whereIn(
    'status', ['open', 'paid']
)->get();
```

`whereNotIn`은 컬럼 값이 배열에 포함되지 않은 경우만 검색됩니다:

```php
$orders = Order::search('Star Trek')->whereNotIn(
    'status', ['closed']
)->get();
```

> [!WARNING]
> 애플리케이션에서 Meilisearch를 사용하는 경우, Scout의 "where" 절을 사용하기 전에 반드시 [filterable 속성](#meilisearch-index-settings)을 미리 설정해야 합니다.

<a name="customizing-the-eloquent-results-query"></a>
#### Eloquent 결과 쿼리 커스터마이즈

Scout가 검색 엔진에서 일치하는 Eloquent 모델 목록을 받아온 뒤, Eloquent는 해당 모델의 기본 키로 실제 레코드를 불러옵니다. 이 과정에서 실행되는 쿼리를 커스터마이즈하려면 `query` 메서드를 사용할 수 있습니다. 이 메서드는 Eloquent 쿼리 빌더 인스턴스를 인자로 받는 클로저를 인자로 받습니다:

```php
use App\Models\Order;
use Illuminate\Database\Eloquent\Builder;

$orders = Order::search('Star Trek')
    ->query(fn (Builder $query) => $query->with('invoices'))
    ->get();
```

서드파티 엔진 사용 시에는 이 콜백이 이미 검색 엔진에서 모델을 받아온 후에 실행되므로, 필터링 용도가 아닌 추가 가공 용도로만 사용해야 합니다. 하지만 데이터베이스 엔진 사용 시에는 `query` 메서드의 제약이 바로 데이터베이스 쿼리에 반영되므로 필터링에도 활용할 수 있습니다.

<a name="pagination"></a>
### 페이지네이션 (Pagination)

모델 컬렉션을 단순히 조회하는 것 외에도, `paginate` 메서드로 검색 결과를 페이지네이션할 수 있습니다. 이 메서드는 [일반 Eloquent 쿼리로 페이지네이션](/docs/12.x/pagination)한 것과 동일하게 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 반환합니다:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->paginate();
```

한 페이지당 모여올 레코드 수를 지정하려면 첫 번째 인자에 값을 전달합니다:

```php
$orders = Order::search('Star Trek')->paginate(15);
```

데이터베이스 엔진에서는 `simplePaginate` 메서드를 사용할 수도 있습니다. 이 메서드는 전체 결과 수를 가져오지 않고, 더 많은 결과가 존재하는지만 확인하여 "이전"/"다음" 링크만 표시합니다. 대형 데이터셋에서 효율적입니다:

```php
$orders = Order::search('Star Trek')->simplePaginate(15);
```

검색 결과와 페이지 링크는 [Blade](/docs/12.x/blade)에서 일반 Eloquent 페이지네이션처럼 렌더링할 수 있습니다:

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

페이지네이션 결과를 JSON으로 받고 싶다면, 라우트나 컨트롤러에서 paginator 인스턴스를 바로 반환하면 됩니다:

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    return Order::search($request->input('query'))->paginate(15);
});
```

> [!WARNING]
> 검색 엔진은 Eloquent 모델의 글로벌 스코프를 인식하지 못하므로, Scout 페이지네이션을 사용하는 애플리케이션에서는 글로벌 스코프 사용을 피하거나, Scout 검색 시 동일한 제약을 다시 적용해야 합니다.

<a name="soft-deleting"></a>
### 소프트 삭제 (Soft Deleting)

인덱싱하는 모델이 [소프트 삭제](/docs/12.x/eloquent#soft-deleting)를 지원하고, 소프트 삭제된 모델도 검색 대상에 포함하려면, `config/scout.php`의 `soft_delete` 옵션을 `true`로 설정합니다:

```php
'soft_delete' => true,
```

이 옵션이 `true`이면, Scout는 소프트 삭제된 모델을 인덱스에서 삭제하지 않고 숨어 있는 `__soft_deleted` 속성을 인덱스 레코드에 설정합니다. 이후 검색할 때 `withTrashed` 또는 `onlyTrashed` 메서드로 소프트 삭제된 레코드 포함 여부를 지정할 수 있습니다:

```php
use App\Models\Order;

// 삭제된 레코드까지 포함해 결과를 가져오기
$orders = Order::search('Star Trek')->withTrashed()->get();

// 삭제된 레코드만 결과로 가져오기
$orders = Order::search('Star Trek')->onlyTrashed()->get();
```

> [!NOTE]
> 소프트 삭제 모델이 `forceDelete`로 완전히 삭제되면, Scout는 해당 레코드를 인덱스에서도 자동으로 삭제합니다.

<a name="customizing-engine-searches"></a>
### 엔진 검색 커스터마이즈 (Customizing Engine Searches)

엔진의 검색 동작을 고급 설정으로 커스터마이즈해야 할 경우, `search` 메서드의 두 번째 인수로 클로저를 전달할 수 있습니다. 예를 들어, Algolia 검색 옵션에 지리 위치 데이터를 추가할 수 있습니다:

```php
use Algolia\AlgoliaSearch\SearchIndex;
use App\Models\Order;

Order::search(
    'Star Trek',
    function (SearchIndex $algolia, string $query, array $options) {
        $options['body']['query']['bool']['filter']['geo_distance'] = [
            'distance' => '1000km',
            'location' => ['lat' => 36, 'lon' => 111],
        ];

        return $algolia->search($query, $options);
    }
)->get();
```

<a name="custom-engines"></a>
## 커스텀 엔진 (Custom Engines)

<a name="writing-the-engine"></a>
#### 엔진 구현

내장된 Scout 검색 엔진이 요구 사항에 맞지 않을 경우, 직접 커스텀 엔진을 구현하고 Scout에 등록할 수 있습니다. 커스텀 엔진은 반드시 `Laravel\Scout\Engines\Engine` 추상 클래스를 상속받아야 하며, 아래의 8개 메서드를 반드시 구현해야 합니다:

```php
use Laravel\Scout\Builder;

abstract public function update($models);
abstract public function delete($models);
abstract public function search(Builder $builder);
abstract public function paginate(Builder $builder, $perPage, $page);
abstract public function mapIds($results);
abstract public function map(Builder $builder, $results, $model);
abstract public function getTotalCount($results);
abstract public function flush($model);
```

각 메서드를 구현하는 법을 익히려면, `Laravel\Scout\Engines\AlgoliaEngine` 클래스의 구현을 참고하면 도움이 됩니다.

<a name="registering-the-engine"></a>
#### 엔진 등록

엔진을 구현했다면, 이제 Scout 엔진 매니저의 `extend` 메서드를 사용하여 해당 엔진을 등록할 수 있습니다. Scout 엔진 매니저는 Laravel 서비스 컨테이너에서 사용할 수 있습니다. 보통 `App\Providers\AppServiceProvider` 또는 애플리케이션이 사용하는 다른 서비스 프로바이더의 `boot` 메서드에서 엔진을 등록하면 됩니다:

```php
use App\ScoutExtensions\MySqlSearchEngine;
use Laravel\Scout\EngineManager;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    resolve(EngineManager::class)->extend('mysql', function () {
        return new MySqlSearchEngine;
    });
}
```

엔진 등록을 마쳤으면, 애플리케이션의 `config/scout.php` 설정 파일에서 default Scout `driver`로 지정할 수 있습니다:

```php
'driver' => 'mysql',
```
