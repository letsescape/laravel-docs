<!-- # Laravel Scout -->
# Laravel Scout

- [Introduction](#introduction)
- [Installation](#installation)
    - [Driver Prerequisites](#driver-prerequisites)
    - [Queueing](#queueing)
- [Configuration](#configuration)
    - [Configuring Model Indexes](#configuring-model-indexes)
    - [Configuring Searchable Data](#configuring-searchable-data)
    - [Configuring The Model ID](#configuring-the-model-id)
    - [Configuring Search Engines Per Model](#configuring-search-engines-per-model)
    - [Identifying Users](#identifying-users)
- [Database / Collection Engines](#database-and-collection-engines)
    - [Database Engine](#database-engine)
    - [Collection Engine](#collection-engine)
- [Indexing](#indexing)
    - [Batch Import](#batch-import)
    - [Adding Records](#adding-records)
    - [Updating Records](#updating-records)
    - [Removing Records](#removing-records)
    - [Pausing Indexing](#pausing-indexing)
    - [Conditionally Searchable Model Instances](#conditionally-searchable-model-instances)
- [Searching](#searching)
    - [Where Clauses](#where-clauses)
    - [Pagination](#pagination)
    - [Soft Deleting](#soft-deleting)
    - [Customizing Engine Searches](#customizing-engine-searches)
- [Custom Engines](#custom-engines)
- [Builder Macros](#builder-macros)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Scout](https://github.com/laravel/scout) provides a simple, driver based solution for adding full-text search to your [Eloquent models](/docs/9.x/eloquent). Using model observers, Scout will automatically keep your search indexes in sync with your Eloquent records. -->
[Laravel Scout](https://github.com/laravel/scout)는 [Eloquent models](/docs/9.x/eloquent)에 전체 텍스트 검색 기능을 손쉽게 추가할 수 있도록 드라이버 기반의 간단한 솔루션을 제공합니다. 모델 옵저버를 활용하여, Scout는 Eloquent 레코드와 검색 인덱스를 항상 자동으로 동기화해줍니다.

<!-- Currently, Scout ships with [Algolia](https://www.algolia.com/), [MeiliSearch](https://www.meilisearch.com), and MySQL / PostgreSQL (`database`) drivers. In addition, Scout includes a "collection" driver that is designed for local development usage and does not require any external dependencies or third-party services. Furthermore, writing custom drivers is simple and you are free to extend Scout with your own search implementations. -->
현재 Scout는 [Algolia](https://www.algolia.com/), [MeiliSearch](https://www.meilisearch.com), 그리고 MySQL / PostgreSQL(`database`) 드라이버를 기본으로 제공합니다. 또한, 외부 의존성 없이 로컬 개발 환경에서 사용할 수 있는 "collection" 드라이버도 포함되어 있습니다. 만약 필요하다면, 커스텀 드라이버도 간편하게 구현하여 Scout 기능을 확장할 수 있습니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- First, install Scout via the Composer package manager: -->
먼저 Composer 패키지 매니저를 사용하여 Scout를 설치합니다.

```shell
composer require laravel/scout
```

<!-- After installing Scout, you should publish the Scout configuration file using the `vendor:publish` Artisan command. This command will publish the `scout.php` configuration file to your application's `config` directory: -->
Scout 설치 후, `vendor:publish` 아티즌 명령어를 실행하여 Scout 설정 파일을 배포합니다. 이 명령어를 실행하면 `scout.php` 설정 파일이 애플리케이션의 `config` 디렉터리에 생성됩니다.

```shell
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

<!-- Finally, add the `Laravel\Scout\Searchable` trait to the model you would like to make searchable. This trait will register a model observer that will automatically keep the model in sync with your search driver: -->
마지막으로, 검색 가능한 모델에 `Laravel\Scout\Searchable` 트레이트를 추가합니다. 이 트레이트는 모델 옵저버를 등록하여, 해당 모델의 데이터가 자동으로 검색 드라이버와 동기화되도록 해줍니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;
}
```

<a name="driver-prerequisites"></a>
<!-- ### Driver Prerequisites -->
### Driver Prerequisites

<a name="algolia"></a>
<!-- #### Algolia -->
#### Algolia

<!-- When using the Algolia driver, you should configure your Algolia `id` and `secret` credentials in your `config/scout.php` configuration file. Once your credentials have been configured, you will also need to install the Algolia PHP SDK via the Composer package manager: -->
Algolia 드라이버를 사용하려면 `config/scout.php` 파일에서 Algolia의 `id`와 `secret` 자격증명을 반드시 설정해야 합니다. 자격증명을 지정한 후, Composer로 Algolia PHP SDK도 설치해야 합니다.

```shell
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
<!-- #### MeiliSearch -->
#### MeiliSearch

<!-- [MeiliSearch](https://www.meilisearch.com) is a blazingly fast and open source search engine. If you aren't sure how to install MeiliSearch on your local machine, you may use [Laravel Sail](/docs/9.x/sail#meilisearch), Laravel's officially supported Docker development environment. -->
[MeiliSearch](https://www.meilisearch.com)는 매우 빠른 오픈소스 검색 엔진입니다. 만약 로컬 환경에 MeiliSearch를 설치하는 방법을 잘 모른다면, [Laravel Sail](/docs/9.x/sail#meilisearch)(Laravel 공식 도커 개발 환경)을 사용할 수 있습니다.

<!-- When using the MeiliSearch driver you will need to install the MeiliSearch PHP SDK via the Composer package manager: -->
MeiliSearch 드라이버를 사용할 때는 Composer로 MeiliSearch PHP SDK를 설치해야 합니다.

```shell
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

<!-- Then, set the `SCOUT_DRIVER` environment variable as well as your MeiliSearch `host` and `key` credentials within your application's `.env` file: -->
그리고 `.env` 파일에 `SCOUT_DRIVER` 환경 변수와, MeiliSearch의 `host`, `key` 자격증명을 다음과 같이 추가합니다.

```ini
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

<!-- For more information regarding MeiliSearch, please consult the [MeiliSearch documentation](https://docs.meilisearch.com/learn/getting_started/quick_start.html). -->
MeiliSearch에 대한 더 자세한 정보는 [MeiliSearch documentation](https://docs.meilisearch.com/learn/getting_started/quick_start.html)를 참고하십시오.

<!-- In addition, you should ensure that you install a version of `meilisearch/meilisearch-php` that is compatible with your MeiliSearch binary version by reviewing [MeiliSearch's documentation regarding binary compatibility](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch). -->
또한, 사용하는 MeiliSearch 바이너리 버전에 호환되는 버전의 `meilisearch/meilisearch-php`를 설치했는지 반드시 [MeiliSearch's documentation regarding binary compatibility](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)를 확인해야 합니다.

> [!WARNING]
> MeiliSearch를 사용하는 애플리케이션에서 Scout를 업그레이드할 때는 [review any additional breaking changes](https://github.com/meilisearch/MeiliSearch/releases)을 반드시 확인해야 합니다.

<a name="queueing"></a>
<!-- ### Queueing -->
### Queueing

<!-- While not strictly required to use Scout, you should strongly consider configuring a [queue driver](/docs/9.x/queues) before using the library. Running a queue worker will allow Scout to queue all operations that sync your model information to your search indexes, providing much better response times for your application's web interface. -->
Scout를 사용하는 데 꼭 필요한 것은 아니지만, [queue driver](/docs/9.x/queues) 설정을 강력히 권장합니다. 큐 워커를 실행하면 모델을 검색 인덱스에 동기화하는 작업을 큐에 담아, 애플리케이션의 웹 인터페이스에서 훨씬 빠른 응답 속도를 얻을 수 있습니다.

<!-- Once you have configured a queue driver, set the value of the `queue` option in your `config/scout.php` configuration file to `true`: -->
큐 드라이버 설정 후에는, `config/scout.php` 파일에서 `queue` 옵션 값을 `true`로 지정합니다.

```
'queue' => true,
```

<!-- Even when the `queue` option is set to `false`, it's important to remember that some Scout drivers like Algolia and Meilisearch always index records asynchronously. Meaning, even though the index operation has completed within your Laravel application, the search engine itself may not reflect the new and updated records immediately. -->
`queue` 옵션을 `false`로 설정해도, Algolia나 Meilisearch와 같은 일부 Scout 드라이버는 항상 비동기식으로 인덱싱을 수행함을 기억해야 합니다. 즉, Laravel 애플리케이션에서는 인덱싱 작업이 완료된 후에도 실제 검색 엔진에서는 변경 내용이 바로 반영되지 않을 수 있습니다.

<!-- To specify the connection and queue that your Scout jobs utilize, you may define the `queue` configuration option as an array: -->
Scout 작업이 사용하는 연결 및 큐를 지정하려면, `queue` 옵션을 배열 형태로 설정할 수도 있습니다.

```
'queue' => [
    'connection' => 'redis',
    'queue' => 'scout'
],
```

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<a name="configuring-model-indexes"></a>
<!-- ### Configuring Model Indexes -->
### Configuring Model Indexes

<!-- Each Eloquent model is synced with a given search "index", which contains all of the searchable records for that model. In other words, you can think of each index like a MySQL table. By default, each model will be persisted to an index matching the model's typical "table" name. Typically, this is the plural form of the model name; however, you are free to customize the model's index by overriding the `searchableAs` method on the model: -->
각 Eloquent 모델은 특정 검색 "인덱스"와 연동되어, 해당 모델의 모든 검색 가능한 레코드가 이 인덱스에 저장됩니다. 즉, 각 인덱스는 MySQL의 테이블처럼 생각할 수 있습니다. 기본적으로 각 모델은 모델의 "테이블" 이름과 같은 이름의 인덱스에 저장됩니다. 보통 모델 이름의 복수형 형태입니다. 하지만 필요에 따라 모델의 `searchableAs` 메서드를 오버라이드해서 인덱스 이름을 원하는 대로 지정할 수 있습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * Get the name of the index associated with the model.
     *
     * @return string
     */
    public function searchableAs()
    {
        return 'posts_index';
    }
}
```

<a name="configuring-searchable-data"></a>
<!-- ### Configuring Searchable Data -->
### Configuring Searchable Data

<!-- By default, the entire `toArray` form of a given model will be persisted to its search index. If you would like to customize the data that is synchronized to the search index, you may override the `toSearchableArray` method on the model: -->
기본적으로, 모델의 `toArray` 형태 전체가 검색 인덱스에 저장됩니다. 만약 동기화할 데이터를 원하는 대로 제어하고 싶다면, 모델에서 `toSearchableArray` 메서드를 오버라이드할 수 있습니다.

```
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
     * @return array
     */
    public function toSearchableArray()
    {
        $array = $this->toArray();

        // Customize the data array...

        return $array;
    }
}
```

<!-- Some search engines such as MeiliSearch will only perform filter operations (`>`, `<`, etc.) on data of the correct type. So, when using these search engines and customizing your searchable data, you should ensure that numeric values are cast to their correct type: -->
MeiliSearch와 같은 일부 검색 엔진은 데이터 타입에 따라(`>`, `<` 등) 필터 연산이 가능한 데이터에 제한을 둡니다. 따라서 이러한 검색 엔진에서 데이터를 커스터마이즈할 경우, 숫자 값은 올바른 타입으로 casting해야 합니다.

```
public function toSearchableArray()
{
    return [
        'id' => (int) $this->id,
        'name' => $this->name,
        'price' => (float) $this->price,
    ];
}
```

<a name="configuring-filterable-data-for-meilisearch"></a>
<!-- #### Configuring Filterable Data & Index Settings (MeiliSearch) -->
#### Configuring Filterable Data & Index Settings (MeiliSearch)

<!-- Unlike Scout's other drivers, MeiliSearch requires you to pre-define index search settings such as filterable attributes, sortable attributes, and [other supported settings fields](https://docs.meilisearch.com/reference/api/settings.html). -->
Scout의 다른 드라이버와 달리, MeiliSearch는 필터링 가능한 속성(filterable attribute), 정렬 가능 속성(sortable attribute), 그리고 [other supported settings fields](https://docs.meilisearch.com/reference/api/settings.html)을 반드시 사전에 인덱스 설정으로 정의해야 합니다.

<!-- Filterable attributes are any attributes you plan to filter on when invoking Scout's `where` method, while sortable attributes are any attributes you plan to sort by when invoking Scout's `orderBy` method. To define your index settings, adjust the `index-settings` portion of your `meilisearch` configuration entry in your application's `scout` configuration file: -->
필터링 가능한 속성은 Scout의 `where` 메서드를 사용할 때 필터링할 속성이며, 정렬 가능한 속성은 `orderBy` 메서드로 정렬할 때 참조되는 속성입니다. 인덱스 설정은 애플리케이션의 `scout` 설정 파일의 `meilisearch` 구성 항목 아래 `index-settings` 부분에서 정의하면 됩니다.

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
            // Other settings fields...
        ],
        Flight::class => [
            'filterableAttributes'=> ['id', 'destination'],
            'sortableAttributes' => ['updated_at'],
        ],
    ],
],
```

<!-- If the model underlying a given index is soft deletable and is included in the `index-settings` array, Scout will automatically include support for filtering on soft deleted models on that index. If you have no other filterable or sortable attributes to define for a soft deletable model index, you may simply add an empty entry to the `index-settings` array for that model: -->
지정한 인덱스에 연결된 모델에 소프트 삭제가 적용되어 있고, 해당 모델이 `index-settings` 배열에 포함되어 있다면, Scout는 해당 인덱스에 소프트 삭제 모델 필터링도 자동으로 지원합니다. 소프트 삭제만 적용하고 별도의 필터/정렬 속성을 지정하지 않으려면, `index-settings` 배열에 아래와 같이 빈 항목으로 추가할 수 있습니다.

```php
'index-settings' => [
    Flight::class => []
],
```

<!-- After configuring your application's index settings, you must invoke the `scout:sync-index-settings` Artisan command. This command will inform MeiliSearch of your currently configured index settings. For convenience, you may wish to make this command part of your deployment process: -->
설정을 마친 후에는 반드시 `scout:sync-index-settings` 아티즌 명령어를 실행해야 합니다. 이 명령어를 통해 MeiliSearch에 현재 설정된 인덱스 옵션이 전달됩니다. 편의상 이 명령어를 배포(deployment) 프로세스에 포함시킬 것을 권장합니다.

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-the-model-id"></a>
<!-- ### Configuring The Model ID -->
### Configuring The Model ID

<!-- By default, Scout will use the primary key of the model as the model's unique ID / key that is stored in the search index. If you need to customize this behavior, you may override the `getScoutKey` and the `getScoutKeyName` methods on the model: -->
Scout는 기본적으로 모델의 기본 키(primary key)를 검색 인덱스에 저장할 모델의 고유 ID/키로 사용합니다. 만약 이 동작을 변경하고 싶다면, 모델에서 `getScoutKey` 및 `getScoutKeyName` 메서드를 오버라이드하면 됩니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * Get the value used to index the model.
     *
     * @return mixed
     */
    public function getScoutKey()
    {
        return $this->email;
    }

    /**
     * Get the key name used to index the model.
     *
     * @return mixed
     */
    public function getScoutKeyName()
    {
        return 'email';
    }
}
```

<a name="configuring-search-engines-per-model"></a>
<!-- ### Configuring Search Engines Per Model -->
### Configuring Search Engines Per Model

<!-- When searching, Scout will typically use the default search engine specified in your application's `scout` configuration file. However, the search engine for a particular model can be changed by overriding the `searchableUsing` method on the model: -->
검색 시 Scout는 보통 애플리케이션의 `scout` 설정 파일에서 지정한 기본 검색 엔진을 사용합니다. 그러나 특정 모델에 대해 사용할 검색 엔진을 바꾸고 싶다면, 모델의 `searchableUsing` 메서드를 오버라이드할 수 있습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\EngineManager;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * Get the engine used to index the model.
     *
     * @return \Laravel\Scout\Engines\Engine
     */
    public function searchableUsing()
    {
        return app(EngineManager::class)->engine('meilisearch');
    }
}
```

<a name="identifying-users"></a>
<!-- ### Identifying Users -->
### Identifying Users

<!-- Scout also allows you to auto identify users when using [Algolia](https://algolia.com). Associating the authenticated user with search operations may be helpful when viewing your search analytics within Algolia's dashboard. You can enable user identification by defining a `SCOUT_IDENTIFY` environment variable as `true` in your application's `.env` file: -->
Scout에서는 [Algolia](https://algolia.com) 사용 시, 검색 작업과 인증된 사용자를 자동으로 연결하여 분석할 수 있습니다. 이 기능을 활성화하면 Algolia의 대시보드에서 검색 분석 시 인증 유저 정보를 참고할 수 있습니다. `.env` 파일에 `SCOUT_IDENTIFY` 환경 변수를 `true`로 지정하면 사용 가능합니다.

```ini
SCOUT_IDENTIFY=true
```

<!-- Enabling this feature this will also pass the request's IP address and your authenticated user's primary identifier to Algolia so this data is associated with any search request that is made by the user. -->
이 기능이 활성화되면 요청의 IP 주소와 인증된 사용자의 고유 식별자가 Algolia로 전송되어, 해당 사용자가 검색할 때마다 이 데이터가 참조됩니다.

<a name="database-and-collection-engines"></a>
<!-- ## Database / Collection Engines -->
## Database / Collection Engines

<a name="database-engine"></a>
<!-- ### Database Engine -->
### Database Engine

> [!WARNING]
> 데이터베이스 엔진은 현재 MySQL 및 PostgreSQL만 지원합니다.

<!-- If your application interacts with small to medium sized databases or has a light workload, you may find it more convenient to get started with Scout's "database" engine. The database engine will use "where like" clauses and full text indexes when filtering results from your existing database to determine the applicable search results for your query. -->
애플리케이션에서 소규모~중간 규모 데이터베이스를 사용하거나, 부하가 적은 경우에는 Scout의 "database" 엔진을 쉽게 시작점으로 사용할 수 있습니다. 데이터베이스 엔진은 "where like" 조건과 전체 텍스트 인덱스를 활용하여 기존 데이터베이스에서 쿼리 결과를 필터링한 후, 해당 검색 결과를 반환합니다.

<!-- To use the database engine, you may simply set the value of the `SCOUT_DRIVER` environment variable to `database`, or specify the `database` driver directly in your application's `scout` configuration file: -->
데이터베이스 엔진을 사용하려면, .env 파일에서 `SCOUT_DRIVER` 환경 변수를 `database`로 지정하거나, 애플리케이션의 `scout` 설정 파일에서 `database` 드라이버를 직접 지정하면 됩니다.

```ini
SCOUT_DRIVER=database
```

<!-- Once you have specified the database engine as your preferred driver, you must [configure your searchable data](#configuring-searchable-data). Then, you may start [executing search queries](#searching) against your models. Search engine indexing, such as the indexing needed to seed Algolia or MeiliSearch indexes, is unnecessary when using the database engine. -->
데이터베이스 엔진을 기본 드라이버로 지정하면, [configure your searchable data](#configuring-searchable-data)을 완료한 뒤 [executing search queries](#searching)이 가능합니다. Algolia나 MeiliSearch와 달리, 인덱스 구축이 별도로 필요하지 않습니다.

<!-- #### Customizing Database Searching Strategies -->
#### Customizing Database Searching Strategies

<!-- By default, the database engine will execute a "where like" query against every model attribute that you have [configured as searchable](#configuring-searchable-data). However, in some situations, this may result in poor performance. Therefore, the database engine's search strategy can be configured so that some specified columns utilize full text search queries or only use "where like" constraints to search the prefixes of strings (`example%`) instead of searching within the entire string (`%example%`). -->
기본적으로 데이터베이스 엔진은 [configured as searchable](#configuring-searchable-data) 모든 속성에 대해 "where like" 쿼리를 실행합니다. 하지만 이 방식은 상황에 따라 성능 저하를 유발할 수 있습니다. 따라서 특정 컬럼은 전체 텍스트 검색을, 또 어떤 컬럼은 문자열 접두어로만 "where like" 제한을 적용하도록 전략을 지정할 수 있습니다(예: `example%`로 접두어 검색, `%example%`처럼 전체 문자열 내부 검색 대상 아님).

<!-- To define this behavior, you may assign PHP attributes to your model's `toSearchableArray` method. Any columns that are not assigned additional search strategy behavior will continue to use the default "where like" strategy: -->
이 동작은 모델의 `toSearchableArray` 메서드에 PHP attributes를 추가해서 정의할 수 있습니다. 별도 전략이 할당되지 않은 컬럼은 기본 "where like" 전략을 사용합니다.

```php
use Laravel\Scout\Attributes\SearchUsingFullText;
use Laravel\Scout\Attributes\SearchUsingPrefix;

/**
 * Get the indexable data array for the model.
 *
 * @return array
 */
#[SearchUsingPrefix(['id', 'email'])]
#[SearchUsingFullText(['bio'])]
public function toSearchableArray()
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
> 컬럼에 전체 텍스트 쿼리 제약을 지정하려면, 반드시 해당 컬럼이 [full text index](/docs/9.x/migrations#available-index-types)를 보유하고 있어야 합니다.

<a name="collection-engine"></a>
<!-- ### Collection Engine -->
### Collection Engine

<!-- While you are free to use the Algolia or MeiliSearch search engines during local development, you may find it more convenient to get started with the "collection" engine. The collection engine will use "where" clauses and collection filtering on results from your existing database to determine the applicable search results for your query. When using this engine, it is not necessary to "index" your searchable models, as they will simply be retrieved from your local database. -->
로컬 개발 환경에서 Algolia나 MeiliSearch를 사용해도 되지만, "collection" 엔진을 사용하는 편이 더 간편할 수 있습니다. 컬렉션 엔진은 기존 데이터베이스에서 결과를 조회한 다음, "where" 절 및 컬렉션 필터링을 이용해 검색 결과를 결정합니다. 이 엔진을 사용할 때는 별도로 검색 인덱싱을 수행할 필요 없이, 검색 가능한 모델이 로컬 데이터베이스에서 바로 조회됩니다.

<!-- To use the collection engine, you may simply set the value of the `SCOUT_DRIVER` environment variable to `collection`, or specify the `collection` driver directly in your application's `scout` configuration file: -->
컬렉션 엔진을 사용하려면, .env 파일의 `SCOUT_DRIVER` 값을 `collection`으로 지정하거나, `scout` 설정 파일에서 `collection` 드라이버를 직접 지정합니다.

```ini
SCOUT_DRIVER=collection
```

<!-- Once you have specified the collection driver as your preferred driver, you may start [executing search queries](#searching) against your models. Search engine indexing, such as the indexing needed to seed Algolia or MeiliSearch indexes, is unnecessary when using the collection engine. -->
컬렉션 드라이버를 선택 후에는, [executing search queries](#searching)이 가능합니다. 이 엔진은 Algolia/MeiliSearch와 달리 별도의 인덱싱 작업이 필요하지 않습니다.

<!-- #### Differences From Database Engine -->
#### Differences From Database Engine

<!-- On first glance, the "database" and "collections" engines are fairly similar. They both interact directly with your database to retrieve search results. However, the collection engine does not utilize full text indexes or `LIKE` clauses to find matching records. Instead, it pulls all possible records and uses Laravel's `Str::is` helper to determine if the search string exists within the model attribute values. -->
겉보기에 "database"와 "collection" 두 엔진은 비슷해 보이지만, 중요한 차이점이 있습니다. 둘 다 DB에서 직접 데이터를 조회하긴 하지만, 컬렉션 엔진은 전체 텍스트 인덱스나 `LIKE` 조건을 활용하지 않고, 가능한 모든 레코드를 조회한 후 Laravel의 `Str::is` 헬퍼를 이용해 검색 문자열이 모델 속성 값에 포함되는지 판별합니다.

<!-- The collection engine is the most portable search engine as it works across all relational databases supported by Laravel (including SQLite and SQL Server); however, it is less efficient than Scout's database engine. -->
컬렉션 엔진은 SQLite, SQL Server 등 Laravel이 지원하는 모든 관계형 DB에서 동작하기 때문에 가장 이식성이 높지만, 성능 면에서는 database 엔진보다 비효율적입니다.

<a name="indexing"></a>
<!-- ## Indexing -->
## Indexing

<a name="batch-import"></a>
<!-- ### Batch Import -->
### Batch Import

<!-- If you are installing Scout into an existing project, you may already have database records you need to import into your indexes. Scout provides a `scout:import` Artisan command that you may use to import all of your existing records into your search indexes: -->
기존 프로젝트에 Scout를 도입했다면, 이미 생성된 DB 레코드를 인덱스에 가져올 필요가 있을 수 있습니다. 이때는 `scout:import` 아티즌 명령어를 사용해 모든 기존 레코드를 검색 인덱스에 임포트할 수 있습니다.

```shell
php artisan scout:import "App\Models\Post"
```

<!-- The `flush` command may be used to remove all of a model's records from your search indexes: -->
모델의 모든 레코드를 검색 인덱스에서 제거하려면, `flush` 명령어를 사용합니다.

```shell
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
<!-- #### Modifying The Import Query -->
#### Modifying The Import Query

<!-- If you would like to modify the query that is used to retrieve all of your models for batch importing, you may define a `makeAllSearchableUsing` method on your model. This is a great place to add any eager relationship loading that may be necessary before importing your models: -->
배치 임포트 시 모든 모델을 가져오는 쿼리를 수정하고 싶다면, 모델에 `makeAllSearchableUsing` 메서드를 정의할 수 있습니다. 예를 들어, 모델 임포트 이전에 관련된 연관관계를 eager 로딩하려는 경우에 적합합니다.

```
/**
 * Modify the query used to retrieve models when making all of the models searchable.
 *
 * @param  \Illuminate\Database\Eloquent\Builder  $query
 * @return \Illuminate\Database\Eloquent\Builder
 */
protected function makeAllSearchableUsing($query)
{
    return $query->with('author');
}
```

<a name="adding-records"></a>
<!-- ### Adding Records -->
### Adding Records

<!-- Once you have added the `Laravel\Scout\Searchable` trait to a model, all you need to do is `save` or `create` a model instance and it will automatically be added to your search index. If you have configured Scout to [use queues](#queueing) this operation will be performed in the background by your queue worker: -->
모델에 `Laravel\Scout\Searchable` 트레이트를 추가한 뒤에는, 단순히 모델 인스턴스를 `save` 또는 `create` 하면 자동으로 검색 인덱스에 추가됩니다. 만약 [use queues](#queueing)했다면, 이 작업은 큐 워커가 백그라운드에서 처리하게 됩니다.

```
use App\Models\Order;

$order = new Order;

// ...

$order->save();
```

<a name="adding-records-via-query"></a>
<!-- #### Adding Records Via Query -->
#### Adding Records Via Query

<!-- If you would like to add a collection of models to your search index via an Eloquent query, you may chain the `searchable` method onto the Eloquent query. The `searchable` method will [chunk the results](/docs/9.x/eloquent#chunking-results) of the query and add the records to your search index. Again, if you have configured Scout to use queues, all of the chunks will be imported in the background by your queue workers: -->
Eloquent 쿼리로 모델 컬렉션을 검색 인덱스에 추가하고 싶으면, `searchable` 메서드를 쿼리에 체이닝해서 사용할 수 있습니다. `searchable` 메서드는 해당 쿼리 결과를 [chunk the results](/docs/9.x/eloquent#chunking-results)로 나누어 인덱스에 추가합니다. 역시 큐를 사용하도록 설정했다면, 모든 청크가 큐 워커에 의해 백그라운드에서 처리됩니다.

```
use App\Models\Order;

Order::where('price', '>', 100)->searchable();
```

<!-- You may also call the `searchable` method on an Eloquent relationship instance: -->
또한 Eloquent 연관관계 인스턴스에서 바로 `searchable`을 호출할 수도 있습니다.

```
$user->orders()->searchable();
```

<!-- Or, if you already have a collection of Eloquent models in memory, you may call the `searchable` method on the collection instance to add the model instances to their corresponding index: -->
이미 메모리에 컬렉션(Eloquent 모델 컬렉션)이 있다면, 컬렉션 인스턴스에서 `searchable`을 호출하여 각 모델을 인덱스에 추가할 수 있습니다.

```
$orders->searchable();
```

> [!NOTE]
> `searchable` 메서드는 "upsert" 작업으로 볼 수 있습니다. 즉, 인덱스에 이미 모델 레코드가 있으면 업데이트되고, 없으면 새로 추가됩니다.

<a name="updating-records"></a>
<!-- ### Updating Records -->
### Updating Records

<!-- To update a searchable model, you only need to update the model instance's properties and `save` the model to your database. Scout will automatically persist the changes to your search index: -->
검색 가능한 모델을 업데이트하려면, 모델 인스턴스의 속성 값을 변경한 뒤 `save` 하면 됩니다. Scout가 자동으로 변경 내용을 검색 인덱스에도 반영해줍니다.

```
use App\Models\Order;

$order = Order::find(1);

// Update the order...

$order->save();
```

<!-- You may also invoke the `searchable` method on an Eloquent query instance to update a collection of models. If the models do not exist in your search index, they will be created: -->
또는, Eloquent 쿼리 인스턴스에서 `searchable`을 호출하여 여러 모델을 일괄 업데이트할 수 있습니다. 인덱스에 해당 모델이 없으면 새로 추가됩니다.

```
Order::where('price', '>', 100)->searchable();
```

<!-- If you would like to update the search index records for all of the models in a relationship, you may invoke the `searchable` on the relationship instance: -->
연관관계 전체에 대해 검색 인덱스를 업데이트하려면, 연관관계 인스턴스에서 `searchable`을 호출하면 됩니다.

```
$user->orders()->searchable();
```

<!-- Or, if you already have a collection of Eloquent models in memory, you may call the `searchable` method on the collection instance to update the model instances in their corresponding index: -->
또는 컬렉션(Eloquent 모델 컬렉션)이 메모리에 있다면, 컬렉션에서 `searchable`을 호출해 인덱스를 업데이트할 수 있습니다.

```
$orders->searchable();
```

<a name="removing-records"></a>
<!-- ### Removing Records -->
### Removing Records

<!-- To remove a record from your index you may simply `delete` the model from the database. This may be done even if you are using [soft deleted](/docs/9.x/eloquent#soft-deleting) models: -->
인덱스에서 레코드를 제거하려면, 데이터베이스에서 해당 모델을 `delete` 하면 됩니다. [soft deleted](/docs/9.x/eloquent#soft-deleting) 모델도 동일하게 동작합니다.

```
use App\Models\Order;

$order = Order::find(1);

$order->delete();
```

<!-- If you do not want to retrieve the model before deleting the record, you may use the `unsearchable` method on an Eloquent query instance: -->
레코드를 먼저 조회하지 않고 바로 삭제하고 싶다면, Eloquent 쿼리에서 `unsearchable` 메서드를 사용할 수 있습니다.

```
Order::where('price', '>', 100)->unsearchable();
```

<!-- If you would like to remove the search index records for all of the models in a relationship, you may invoke the `unsearchable` on the relationship instance: -->
연관관계 전체에 대해 검색 인덱스에서 레코드를 제거하려면, 연관관계 인스턴스에서 `unsearchable`을 호출합니다.

```
$user->orders()->unsearchable();
```

<!-- Or, if you already have a collection of Eloquent models in memory, you may call the `unsearchable` method on the collection instance to remove the model instances from their corresponding index: -->
또는 컬렉션이 메모리에 있다면, 컬렉션에서 `unsearchable`을 호출하여 해당 모델 인스턴스들을 인덱스에서 제거할 수 있습니다.

```
$orders->unsearchable();
```

<a name="pausing-indexing"></a>
<!-- ### Pausing Indexing -->
### Pausing Indexing

<!-- Sometimes you may need to perform a batch of Eloquent operations on a model without syncing the model data to your search index. You may do this using the `withoutSyncingToSearch` method. This method accepts a single closure which will be immediately executed. Any model operations that occur within the closure will not be synced to the model's index: -->
때로는 한 번에 여러 Eloquent 작업을 수행하되, 이 작업들이 일시적으로 검색 인덱스와 동기화되지 않도록 하고 싶을 수 있습니다. 이럴 때는 `withoutSyncingToSearch` 메서드를 사용하면 됩니다. 이 메서드는 하나의 클로저를 인자로 받고, 해당 클로저 안에서 일어난 모든 모델 작업은 인덱스로 동기화되지 않습니다.

```
use App\Models\Order;

Order::withoutSyncingToSearch(function () {
    // Perform model actions...
});
```

<a name="conditionally-searchable-model-instances"></a>
<!-- ### Conditionally Searchable Model Instances -->
### Conditionally Searchable Model Instances

<!-- Sometimes you may need to only make a model searchable under certain conditions. For example, imagine you have `App\Models\Post` model that may be in one of two states: "draft" and "published". You may only want to allow "published" posts to be searchable. To accomplish this, you may define a `shouldBeSearchable` method on your model: -->
모델이 특정 조건을 만족할 때만 검색 인덱스에 포함되도록 제어하고 싶을 때가 있습니다. 예를 들어, `App\Models\Post` 모델이 "draft" 또는 "published" 상태일 수 있다고 가정해 보겠습니다. "published" 상태인 포스트만 검색 가능하게 하려면, 모델에 `shouldBeSearchable` 메서드를 정의하면 됩니다.

```
/**
 * Determine if the model should be searchable.
 *
 * @return bool
 */
public function shouldBeSearchable()
{
    return $this->isPublished();
}
```

<!-- The `shouldBeSearchable` method is only applied when manipulating models through the `save` and `create` methods, queries, or relationships. Directly making models or collections searchable using the `searchable` method will override the result of the `shouldBeSearchable` method. -->
`shouldBeSearchable` 메서드는 `save`, `create` 메서드, 쿼리, 또는 연관관계를 통한 모델 조작 시에만 적용됩니다. 컬렉션이나 모델을 직접 `searchable`로 만들면 `shouldBeSearchable` 메서드의 결과가 무시됩니다.

> [!WARNING]
> `shouldBeSearchable` 메서드는 Scout의 "database" 엔진에서는 적용되지 않습니다. "database" 엔진에서는 모든 검색 가능 데이터가 DB에 저장되기 때문입니다. database 엔진에서 유사한 기능이 필요하다면 [where clauses](#where-clauses)을 사용해야 합니다.

<a name="searching"></a>
<!-- ## Searching -->
## Searching

<!-- You may begin searching a model using the `search` method. The search method accepts a single string that will be used to search your models. You should then chain the `get` method onto the search query to retrieve the Eloquent models that match the given search query: -->
모델을 검색하려면 `search` 메서드를 사용합니다. 이 메서드는 검색어를 인자로 받아 모델을 검색합니다. 이후 `get` 메서드를 체이닝하여, 해당 쿼리에 매칭되는 Eloquent 모델들을 조회합니다.

```
use App\Models\Order;

$orders = Order::search('Star Trek')->get();
```

<!-- Since Scout searches return a collection of Eloquent models, you may even return the results directly from a route or controller and they will automatically be converted to JSON: -->
Scout의 검색 결과는 Eloquent 모델 컬렉션으로 반환되므로, 라우트나 컨트롤러에서 결과를 그대로 리턴하면 자동으로 JSON 형태로 변환됩니다.

```
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/search', function (Request $request) {
    return Order::search($request->search)->get();
});
```

<!-- If you would like to get the raw search results before they are converted to Eloquent models, you may use the `raw` method: -->
Eloquent 모델로 변환되기 전의 원시 검색 결과를 직접 받고 싶다면 `raw` 메서드를 사용할 수 있습니다.

```
$orders = Order::search('Star Trek')->raw();
```

<a name="custom-indexes"></a>
<!-- #### Custom Indexes -->
#### Custom Indexes

<!-- Search queries will typically be performed on the index specified by the model's [`searchableAs`](#configuring-model-indexes) method. However, you may use the `within` method to specify a custom index that should be searched instead: -->
검색 쿼리는 보통 모델의 [`searchableAs`](#configuring-model-indexes) 메서드에서 지정한 인덱스에서 수행됩니다. 하지만 `within` 메서드를 사용하면 특정 커스텀 인덱스에서 검색할 수 있습니다.

```
$orders = Order::search('Star Trek')
    ->within('tv_shows_popularity_desc')
    ->get();
```

<a name="where-clauses"></a>
<!-- ### Where Clauses -->
### Where Clauses

<!-- Scout allows you to add simple "where" clauses to your search queries. Currently, these clauses only support basic numeric equality checks and are primarily useful for scoping search queries by an owner ID: -->
Scout는 검색 쿼리에 간단한 "where" 절을 추가할 수 있는 기능을 제공합니다. 현재 이 where 절은 기본적인 숫자형 동등(equal) 연산만 지원하며, 보통 소유자 ID 등으로 범위를 제한할 때 활용합니다.

```
use App\Models\Order;

$orders = Order::search('Star Trek')->where('user_id', 1)->get();
```

<!-- You may use the `whereIn` method to constrain results against a given set of values: -->
`whereIn` 메서드를 사용하면 주어진 값 집합에 매칭되는 결과만 검색할 수 있습니다.

```
$orders = Order::search('Star Trek')->whereIn(
    'status', ['paid', 'open']
)->get();
```

<!-- Since a search index is not a relational database, more advanced "where" clauses are not currently supported. -->
검색 인덱스는 관계형 DB가 아니기 때문에, 복잡한 조건의 where 절은 사용할 수 없습니다.

> [!WARNING]
> 애플리케이션에서 MeiliSearch를 사용 중이라면, 반드시 Scout의 "where" 절을 사용하기 전에 [filterable attributes](#configuring-filterable-data-for-meilisearch) 설정을 완료해야 합니다.

<a name="pagination"></a>
<!-- ### Pagination -->
### Pagination

<!-- In addition to retrieving a collection of models, you may paginate your search results using the `paginate` method. This method will return an `Illuminate\Pagination\LengthAwarePaginator` instance just as if you had [paginated a traditional Eloquent query](/docs/9.x/pagination): -->
컬렉션을 단순 조회하는 대신, `paginate` 메서드를 사용해 검색 결과를 페이지네이션할 수 있습니다. 이 메서드는 [paginated a traditional Eloquent query](/docs/9.x/pagination)과 동일하게 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 반환합니다.

```
use App\Models\Order;

$orders = Order::search('Star Trek')->paginate();
```

<!-- You may specify how many models to retrieve per page by passing the amount as the first argument to the `paginate` method: -->
한 페이지에 가져올 모델 수를 지정하려면 `paginate` 메서드의 첫 번째 인자로 개수를 넘겨줍니다.

```
$orders = Order::search('Star Trek')->paginate(15);
```

<!-- Once you have retrieved the results, you may display the results and render the page links using [Blade](/docs/9.x/blade) just as if you had paginated a traditional Eloquent query: -->
검색 결과를 받아 [Blade](/docs/9.x/blade) 템플릿에서 페이지네이션 링크까지 기존 Eloquent 쿼리와 동일하게 사용할 수 있습니다.

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

<!-- Of course, if you would like to retrieve the pagination results as JSON, you may return the paginator instance directly from a route or controller: -->
물론, 페이지네이션 결과를 JSON으로 반환하고 싶다면 라우트나 컨트롤러에서 paginator 인스턴스를 그대로 반환하면 됩니다.

```
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    return Order::search($request->input('query'))->paginate(15);
});
```

> [!WARNING]
> 검색 엔진은 Eloquent 모델의 글로벌 스코프 정의를 알지 못하므로, Scout의 페이지네이션 기능을 사용하는 앱에서는 글로벌 스코프 사용을 피해야 합니다. 또는 검색 시 Scout에서도 동일하게 스코프 제약조건을 재구현해야 합니다.

<a name="soft-deleting"></a>
<!-- ### Soft Deleting -->
### Soft Deleting

<!-- If your indexed models are [soft deleting](/docs/9.x/eloquent#soft-deleting) and you need to search your soft deleted models, set the `soft_delete` option of the `config/scout.php` configuration file to `true`: -->
색인화된 모델에 [soft deleting](/docs/9.x/eloquent#soft-deleting)를 적용했고, 이 소프트 삭제 모델까지 검색하고 싶다면 `config/scout.php` 파일의 `soft_delete` 옵션을 `true`로 설정하면 됩니다.

```
'soft_delete' => true,
```

<!-- When this configuration option is `true`, Scout will not remove soft deleted models from the search index. Instead, it will set a hidden `__soft_deleted` attribute on the indexed record. Then, you may use the `withTrashed` or `onlyTrashed` methods to retrieve the soft deleted records when searching: -->
이 옵션이 `true`일 경우, Scout는 소프트 삭제 모델을 인덱스에서 제거하지 않고, 색인 레코드에 숨겨진 `__soft_deleted` 속성을 설정합니다. 그 다음, 검색 시 `withTrashed` 또는 `onlyTrashed` 메서드를 사용하여 소프트 삭제된 레코드도 함께 가져오거나, 소프트 삭제 레코드만 조회할 수 있습니다.

```
use App\Models\Order;

// Include trashed records when retrieving results...
$orders = Order::search('Star Trek')->withTrashed()->get();

// Only include trashed records when retrieving results...
$orders = Order::search('Star Trek')->onlyTrashed()->get();
```

> [!NOTE]
> 소프트 삭제 모델을 `forceDelete`로 완전 삭제하면, Scout가 인덱스에서 해당 레코드를 자동으로 제거합니다.

<a name="customizing-engine-searches"></a>
<!-- ### Customizing Engine Searches -->
### Customizing Engine Searches

<!-- If you need to perform advanced customization of the search behavior of an engine you may pass a closure as the second argument to the `search` method. For example, you could use this callback to add geo-location data to your search options before the search query is passed to Algolia: -->
검색 엔진에서 더욱 고급 검색 동작을 구현하고 싶을 때는, `search` 메서드의 두 번째 인자로 클로저(callback)를 넘길 수 있습니다. 예를 들어, 이 콜백에서 검색 쿼리가 Algolia로 전달되기 전에 지리정보 데이터(geo-location data)를 검색 옵션에 추가할 수도 있습니다.

```
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

<a name="customizing-the-eloquent-results-query"></a>
<!-- #### Customizing The Eloquent Results Query -->
#### Customizing The Eloquent Results Query

<!-- After Scout retrieves a list of matching Eloquent models from your application's search engine, Eloquent is used to retrieve all of the matching models by their primary keys. You may customize this query by invoking the `query` method. The `query` method accepts a closure that will receive the Eloquent query builder instance as an argument: -->
Scout가 검색 엔진으로부터 일치하는 Eloquent 기본 키 목록을 받아오면, Eloquent를 통해 실제 모델을 조회합니다. 이 쿼리를 커스터마이즈하려면 `query` 메서드를 사용할 수 있으며, `query` 메서드는 쿼리 빌더 인스턴스를 인자로 받는 클로저를 전달받습니다.

```php
use App\Models\Order;

$orders = Order::search('Star Trek')
    ->query(fn ($query) => $query->with('invoices'))
    ->get();
```

<!-- Since this callback is invoked after the relevant models have already been retrieved from your application's search engine, the `query` method should not be used for "filtering" results. Instead, you should use [Scout where clauses](#where-clauses). -->
이 콜백은 검색 엔진에서 모델 목록을 이미 받은 후 호출되므로, `query` 메서드를 결과 "필터링" 용도로는 사용하지 않고 [Scout where clauses](#where-clauses)을 활용하는 것이 좋습니다.

<a name="custom-engines"></a>
<!-- ## Custom Engines -->
## Custom Engines

<a name="writing-the-engine"></a>
<!-- #### Writing The Engine -->
#### Writing The Engine

<!-- If one of the built-in Scout search engines doesn't fit your needs, you may write your own custom engine and register it with Scout. Your engine should extend the `Laravel\Scout\Engines\Engine` abstract class. This abstract class contains eight methods your custom engine must implement: -->
기본 제공되는 Scout의 검색 엔진 외에, 직접 커스텀 엔진을 구현하여 등록할 수도 있습니다. 커스텀 엔진은 `Laravel\Scout\Engines\Engine` 추상 클래스를 상속해야 하며, 다음 8가지 메서드를 반드시 구현해야 합니다.

```
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

<!-- You may find it helpful to review the implementations of these methods on the `Laravel\Scout\Engines\AlgoliaEngine` class. This class will provide you with a good starting point for learning how to implement each of these methods in your own engine. -->
이 메서드 각각의 구현 방법은 `Laravel\Scout\Engines\AlgoliaEngine` 클래스를 참고하면 이해에 도움이 됩니다. 각 메서드를 새로운 엔진에서 어떻게 구현하는지 예시로 삼을 수 있습니다.

<a name="registering-the-engine"></a>
<!-- #### Registering The Engine -->
#### Registering The Engine

<!-- Once you have written your custom engine, you may register it with Scout using the `extend` method of the Scout engine manager. Scout's engine manager may be resolved from the Laravel service container. You should call the `extend` method from the `boot` method of your `App\Providers\AppServiceProvider` class or any other service provider used by your application: -->
커스텀 엔진을 구현했다면, Scout 엔진 매니저의 `extend` 메서드를 사용해서 등록하면 됩니다. Scout 엔진 매니저는 Laravel 서비스 컨테이너에서 해결할 수 있습니다. `extend` 메서드는 보통 `App\Providers\AppServiceProvider`의 `boot` 메서드나, 기타 서비스 프로바이더에서 호출할 수 있습니다.

```
use App\ScoutExtensions\MySqlSearchEngine
use Laravel\Scout\EngineManager;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    resolve(EngineManager::class)->extend('mysql', function () {
        return new MySqlSearchEngine;
    });
}
```

<!-- Once your engine has been registered, you may specify it as your default Scout `driver` in your application's `config/scout.php` configuration file: -->
등록이 끝나면, 애플리케이션의 `config/scout.php` 설정 파일에서 기본 Scout `driver`를 해당 이름으로 지정하면 됩니다.

```
'driver' => 'mysql',
```

<a name="builder-macros"></a>
<!-- ## Builder Macros -->
## Builder Macros

<!-- If you would like to define a custom Scout search builder method, you may use the `macro` method on the `Laravel\Scout\Builder` class. Typically, "macros" should be defined within a [service provider's](/docs/9.x/providers) `boot` method: -->
Scout의 검색 빌더에 커스텀 메서드를 정의하고 싶을 때는, `Laravel\Scout\Builder` 클래스의 `macro` 메서드를 사용할 수 있습니다. 보통 이런 "매크로"는 [service provider's](/docs/9.x/providers)의 `boot` 메서드 안에서 정의합니다.

```
use Illuminate\Support\Facades\Response;
use Illuminate\Support\ServiceProvider;
use Laravel\Scout\Builder;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Builder::macro('count', function () {
        return $this->engine()->getTotalCount(
            $this->engine()->search($this)
        );
    });
}
```

<!-- The `macro` function accepts a macro name as its first argument and a closure as its second argument. The macro's closure will be executed when calling the macro name from a `Laravel\Scout\Builder` implementation: -->
`macro` 함수는 첫 번째 인자로 매크로 이름, 두 번째 인자로 클로저를 받습니다. 정의된 매크로 이름을 `Laravel\Scout\Builder` 인스턴스에서 호출하면 해당 클로저가 실행됩니다.

```
use App\Models\Order;

Order::search('Star Trek')->count();
```
