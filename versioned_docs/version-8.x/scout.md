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
    - [Identifying Users](#identifying-users)
- [Local Development](#local-development)
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

<!-- [Laravel Scout](https://github.com/laravel/scout) provides a simple, driver based solution for adding full-text search to your [Eloquent models](/docs/8.x/eloquent). Using model observers, Scout will automatically keep your search indexes in sync with your Eloquent records. -->
[Laravel Scout](https://github.com/laravel/scout)는 [Eloquent models](/docs/8.x/eloquent)에 전체 텍스트 검색 기능을 쉽게 추가할 수 있도록 드라이버 기반의 간단한 솔루션을 제공합니다. Scout는 모델 옵저버를 활용하여, Eloquent 레코드와 검색 인덱스가 자동으로 동기화되도록 해줍니다.

<!-- Currently, Scout ships with [Algolia](https://www.algolia.com/) and [MeiliSearch](https://www.meilisearch.com) drivers. In addition, Scout includes a "collection" driver that is designed for local development usage and does not require any external dependencies or third-party services. Furthermore, writing custom drivers is simple and you are free to extend Scout with your own search implementations. -->
현재 Scout는 [Algolia](https://www.algolia.com/)와 [MeiliSearch](https://www.meilisearch.com) 드라이버를 기본으로 제공합니다. 또한, 외부 의존성이나 써드파티 서비스 없이 로컬 개발에 사용할 수 있도록 설계된 "콜렉션(collection)" 드라이버도 포함되어 있습니다. 추가로, 직접 커스텀 드라이버를 작성하는 작업도 간단하므로, 여러분만의 검색 구현으로 Scout를 확장할 수 있습니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- First, install Scout via the Composer package manager: -->
먼저, Composer 패키지 매니저를 통해 Scout를 설치합니다.

```
composer require laravel/scout
```

<!-- After installing Scout, you should publish the Scout configuration file using the `vendor:publish` Artisan command. This command will publish the `scout.php` configuration file to your application's `config` directory: -->
Scout 설치 후, `vendor:publish` Artisan 명령어를 사용해 Scout 설정 파일을 배포해야 합니다. 이 명령어를 실행하면 `scout.php` 설정 파일이 애플리케이션의 `config` 디렉토리에 생성됩니다.

```
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

<!-- Finally, add the `Laravel\Scout\Searchable` trait to the model you would like to make searchable. This trait will register a model observer that will automatically keep the model in sync with your search driver: -->
마지막으로, 검색 가능한 모델에 `Laravel\Scout\Searchable` 트레이트(trait)를 추가합니다. 이 트레이트는 모델 옵저버를 등록하여, 해당 모델이 자동으로 검색 드라이버와 동기화되도록 만들어줍니다.

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
Algolia 드라이버를 사용할 경우, 우선 `config/scout.php` 설정 파일에서 Algolia의 `id`와 `secret` 자격 증명을 설정해야 합니다. 자격 증명을 모두 입력한 뒤, Composer를 통해 Algolia PHP SDK도 설치해야 합니다.

```
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
<!-- #### MeiliSearch -->
#### MeiliSearch

<!-- [MeiliSearch](https://www.meilisearch.com) is a blazingly fast and open source search engine. If you aren't sure how to install MeiliSearch on your local machine, you may use [Laravel Sail](/docs/8.x/sail#meilisearch), Laravel's officially supported Docker development environment. -->
[MeiliSearch](https://www.meilisearch.com)는 매우 빠른 오픈 소스 검색 엔진입니다. 아직 로컬 환경에 MeiliSearch를 설치하는 방법을 잘 모른다면, Laravel에서 공식적으로 지원하는 Docker 개발 환경인 [Laravel Sail](/docs/8.x/sail#meilisearch)을 활용할 수 있습니다.

<!-- When using the MeiliSearch driver you will need to install the MeiliSearch PHP SDK via the Composer package manager: -->
MeiliSearch 드라이버를 사용할 경우, Composer로 MeiliSearch PHP SDK를 설치해야 합니다.

```
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

<!-- Then, set the `SCOUT_DRIVER` environment variable as well as your MeiliSearch `host` and `key` credentials within your application's `.env` file: -->
그리고 애플리케이션의 `.env` 파일에 `SCOUT_DRIVER` 환경 변수와 MeiliSearch의 `host`, `key` 자격 증명을 다음과 같이 설정합니다.

```
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

<!-- For more information regarding MeiliSearch, please consult the [MeiliSearch documentation](https://docs.meilisearch.com/learn/getting_started/quick_start.html). -->
MeiliSearch에 대한 자세한 내용은 [MeiliSearch documentation](https://docs.meilisearch.com/learn/getting_started/quick_start.html)를 참고하시기 바랍니다.

<!-- In addition, you should ensure that you install a version of `meilisearch/meilisearch-php` that is compatible with your MeiliSearch binary version by reviewing [MeiliSearch's documentation regarding binary compatibility](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch). -->
또한, 설치하는 `meilisearch/meilisearch-php` 패키지의 버전이 현재 사용하는 MeiliSearch 바이너리 버전과 호환되는지 반드시 [MeiliSearch's documentation regarding binary compatibility](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)를 확인해야 합니다.

> [!NOTE]
> MeiliSearch를 사용하는 애플리케이션에서 Scout를 업그레이드할 때는, 반드시 MeiliSearch 서비스 자체에 [review any additional breaking changes](https://github.com/meilisearch/MeiliSearch/releases)가 있는지 확인하시기 바랍니다.

<a name="queueing"></a>
<!-- ### Queueing -->
### Queueing

<!-- While not strictly required to use Scout, you should strongly consider configuring a [queue driver](/docs/8.x/queues) before using the library. Running a queue worker will allow Scout to queue all operations that sync your model information to your search indexes, providing much better response times for your application's web interface. -->
Scout를 반드시 큐와 함께 사용해야 하는 것은 아니지만, [queue driver](/docs/8.x/queues)를 별도로 설정하는 것을 강력히 권장합니다. 큐 워커를 실행하면, 모델 정보와 검색 인덱스 동기화 작업이 큐를 통해 처리되어, 애플리케이션의 웹 인터페이스 반응 속도가 훨씬 더 좋아집니다.

<!-- Once you have configured a queue driver, set the value of the `queue` option in your `config/scout.php` configuration file to `true`: -->
큐 드라이버를 설정했다면, `config/scout.php` 파일에서 `queue` 옵션 값을 `true`로 변경합니다.

```
'queue' => true,
```

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<a name="configuring-model-indexes"></a>
<!-- ### Configuring Model Indexes -->
### Configuring Model Indexes

<!-- Each Eloquent model is synced with a given search "index", which contains all of the searchable records for that model. In other words, you can think of each index like a MySQL table. By default, each model will be persisted to an index matching the model's typical "table" name. Typically, this is the plural form of the model name; however, you are free to customize the model's index by overriding the `searchableAs` method on the model: -->
각 Eloquent 모델은 특정 검색 "인덱스(index)"와 동기화됩니다. 이 인덱스에는 해당 모델의 모든 검색 가능한 레코드들이 저장됩니다. 각 인덱스는 MySQL의 테이블과 유사하게 생각할 수 있습니다. 기본적으로, 각 모델은 모델의 일반적인 테이블명과 같은 이름의 인덱스에 저장됩니다. 보통 모델 이름의 복수형이 사용되지만, 모델에서 `searchableAs` 메서드를 오버라이드하여 인덱스명을 자유롭게 지정할 수 있습니다.

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
기본적으로 모델의 `toArray` 결과 전체가 검색 인덱스에 저장됩니다. 만약 검색 인덱스에 동기화할 데이터를 커스터마이즈하고 싶다면, 모델에서 `toSearchableArray` 메서드를 오버라이드하면 됩니다.

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

<a name="configuring-the-model-id"></a>
<!-- ### Configuring The Model ID -->
### Configuring The Model ID

<!-- By default, Scout will use the primary key of the model as model's unique ID / key that is stored in the search index. If you need to customize this behavior, you may override the `getScoutKey` and the `getScoutKeyName` methods on the model: -->
Scout는 기본적으로 모델의 기본 키(primary key)를 검색 인덱스에 저장되는 해당 모델의 고유 ID/키로 사용합니다. 이 동작을 변경하려면, 모델에서 `getScoutKey`와 `getScoutKeyName` 메서드를 오버라이드할 수 있습니다.

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

<a name="identifying-users"></a>
<!-- ### Identifying Users -->
### Identifying Users

<!-- Scout also allows you to auto identify users when using [Algolia](https://algolia.com). Associating the authenticated user with search operations may be helpful when viewing your search analytics within Algolia's dashboard. You can enable user identification by defining a `SCOUT_IDENTIFY` environment variable as `true` in your application's `.env` file: -->
Scout는 [Algolia](https://algolia.com)를 사용할 때 사용자를 자동으로 식별하도록 설정할 수 있습니다. 인증된 사용자를 검색 작업과 연결하면 Algolia의 대시보드에서 검색 분석 정보를 확인할 때 도움이 됩니다. 이 기능을 활성화하려면 애플리케이션의 `.env` 파일에 `SCOUT_IDENTIFY` 환경 변수를 `true`로 추가하십시오.

```
SCOUT_IDENTIFY=true
```

<!-- Enabling this feature this will also pass the request's IP address and your authenticated user's primary identifier to Algolia so this data is associated with any search request that is made by the user. -->
이 기능을 활성화하면, 요청한 사용자의 IP 주소와 인증된 사용자의 기본 식별자가 Algolia로 함께 전송되어, 해당 사용자가 수행한 각 검색 요청과 연결됩니다.

<a name="local-development"></a>
<!-- ## Local Development -->
## Local Development

<!-- While you are free to use the Algolia or MeiliSearch search engines during local development, you may find it more convenient to get started with the "collection" engine. The collection engine will use "where" clauses and collection filtering on results from your existing database to determine the applicable search results for your query. When using this engine, it is not necessary to "index" your searchable models, as they will simply be retrieved from your local database. -->
로컬 개발 중에도 Algolia나 MeiliSearch 검색 엔진을 사용할 수 있지만, "collection" 엔진을 사용하면 더 간편하게 시작할 수 있습니다. collection 엔진은 기존 데이터베이스에서 결과를 받아와 "where" 조건과 컬렉션 필터링을 사용해 검색 결과를 도출합니다. 이 엔진을 사용할 때는, 별도로 검색 가능한 모델을 "인덱싱"할 필요 없이, 로컬 데이터베이스에서 직접 데이터를 조회해올 수 있습니다.

<!-- To use the collection engine, you may simply set the value of the `SCOUT_DRIVER` environment variable to `collection`, or specify the `collection` driver directly in your application's `scout` configuration file: -->
collection 엔진을 사용하려면, 환경변수 `SCOUT_DRIVER`의 값을 `collection`으로 설정하거나, 애플리케이션의 `scout` 설정 파일에서 `collection` 드라이버를 직접 지정하면 됩니다.

```ini
SCOUT_DRIVER=collection
```

<!-- Once you have specified the collection driver as your preferred driver, you may start [executing search queries](#searching) against your models. Search engine indexing, such as the indexing needed to seed Algolia or MeiliSearch indexes, is unnecessary when using the collection engine. -->
이제 collection 드라이버가 설정되었다면, [executing search queries](#searching)을 바로 시작할 수 있습니다. Algolia나 MeiliSearch 인덱싱처럼 별도의 인덱싱 작업 없이 곧바로 사용할 수 있습니다.

<a name="indexing"></a>
<!-- ## Indexing -->
## Indexing

<a name="batch-import"></a>
<!-- ### Batch Import -->
### Batch Import

<!-- If you are installing Scout into an existing project, you may already have database records you need to import into your indexes. Scout provides a `scout:import` Artisan command that you may use to import all of your existing records into your search indexes: -->
기존 프로젝트에 Scout를 도입할 경우, 이미 존재하는 데이터베이스 레코드를 전체 인덱스에 임포트해야 할 수 있습니다. 이럴 때는 Scout가 제공하는 `scout:import` Artisan 명령어를 사용해, 기존 레코드를 모두 검색 인덱스로 가져올 수 있습니다.

```
php artisan scout:import "App\Models\Post"
```

<!-- The `flush` command may be used to remove all of a model's records from your search indexes: -->
모델의 모든 레코드를 검색 인덱스에서 제거하려면, `flush` 명령어를 사용할 수 있습니다.

```
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
<!-- #### Modifying The Import Query -->
#### Modifying The Import Query

<!-- If you would like to modify the query that is used to retrieve all of your models for batch importing, you may define a `makeAllSearchableUsing` method on your model. This is a great place to add any eager relationship loading that may be necessary before importing your models: -->
일괄 임포트에 사용할 쿼리를 커스터마이징하고 싶다면, 모델에 `makeAllSearchableUsing` 메서드를 정의하면 됩니다. 예를 들어, 임포트 전에 Eager 로딩이 필요한 연관관계를 미리 불러올 수 있습니다.

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
`Laravel\Scout\Searchable` 트레이트가 추가된 모델은, 단순히 인스턴스를 `save` 혹은 `create`만 하면 자동으로 검색 인덱스에 추가됩니다. 만약 Scout를 [use queues](#queueing), 이 작업은 백그라운드 큐 워커가 처리합니다.

```
use App\Models\Order;

$order = new Order;

// ...

$order->save();
```

<a name="adding-records-via-query"></a>
<!-- #### Adding Records Via Query -->
#### Adding Records Via Query

<!-- If you would like to add a collection of models to your search index via an Eloquent query, you may chain the `searchable` method onto the Eloquent query. The `searchable` method will [chunk the results](/docs/8.x/eloquent#chunking-results) of the query and add the records to your search index. Again, if you have configured Scout to use queues, all of the chunks will be imported in the background by your queue workers: -->
Eloquent 쿼리를 통해 다수의 모델을 한 번에 검색 인덱스에 추가하고 싶을 때는 Eloquent 쿼리 뒤에 `searchable` 메서드를 체이닝하면 됩니다. `searchable` 메서드는 쿼리 결과를 자동으로 [chunk the results](/docs/8.x/eloquent#chunking-results)하여, 각 레코드를 인덱스에 추가합니다. 큐가 설정되어 있다면, 모든 청크는 큐 워커가 백그라운드에서 임포트합니다.

```
use App\Models\Order;

Order::where('price', '>', 100)->searchable();
```

<!-- You may also call the `searchable` method on an Eloquent relationship instance: -->
Eloquent 연관관계 인스턴스에도 `searchable` 메서드를 사용할 수 있습니다.

```
$user->orders()->searchable();
```

<!-- Or, if you already have a collection of Eloquent models in memory, you may call the `searchable` method on the collection instance to add the model instances to their corresponding index: -->
이미 Eloquent 모델 컬렉션을 메모리에 가지고 있다면, 컬렉션 인스턴스에 바로 `searchable` 메서드를 호출해 해당 모델들을 인덱스에 추가할 수 있습니다.

```
$orders->searchable();
```

> [!TIP]
> `searchable` 메서드는 "upsert"(있으면 업데이트, 없으면 새로 추가) 동작을 수행합니다. 이미 인덱스에 존재한다면 업데이트되고, 없으면 새로 추가됩니다.

<a name="updating-records"></a>
<!-- ### Updating Records -->
### Updating Records

<!-- To update a searchable model, you only need to update the model instance's properties and `save` the model to your database. Scout will automatically persist the changes to your search index: -->
검색 가능한 모델을 업데이트하려면, 해당 인스턴스의 속성 값을 수정한 뒤 데이터베이스에 `save`만 하면 됩니다. Scout가 자동으로 변경 사항을 인덱스에도 반영합니다.

```
use App\Models\Order;

$order = Order::find(1);

// Update the order...

$order->save();
```

<!-- You may also invoke the `searchable` method on an Eloquent query instance to update a collection of models. If the models do not exist in your search index, they will be created: -->
Eloquent 쿼리 인스턴스에서 `searchable` 메서드를 호출해 여러 모델을 한 번에 업데이트할 수도 있습니다. 만약 인덱스에 해당 모델이 없다면 새로 추가됩니다.

```
Order::where('price', '>', 100)->searchable();
```

<!-- If you would like to update the search index records for all of the models in a relationship, you may invoke the `searchable` on the relationship instance: -->
연관관계 인스턴스에 대해서도 `searchable`을 호출해, 모든 연관 모델의 검색 인덱스를 업데이트할 수 있습니다.

```
$user->orders()->searchable();
```

<!-- Or, if you already have a collection of Eloquent models in memory, you may call the `searchable` method on the collection instance to update the model instances in their corresponding index: -->
이미 Eloquent 모델 컬렉션이 있다면, 컬렉션 인스턴스에 `searchable`을 호출하여 해당 모델 인스턴스들을 인덱스에 업데이트합니다.

```
$orders->searchable();
```

<a name="removing-records"></a>
<!-- ### Removing Records -->
### Removing Records

<!-- To remove a record from your index you may simply `delete` the model from the database. This may be done even if you are using [soft deleted](/docs/8.x/eloquent#soft-deleting) models: -->
인덱스에서 레코드를 제거하려면 모델을 데이터베이스에서 `delete`하면 됩니다. [soft deleted](/docs/8.x/eloquent#soft-deleting) 모델을 사용하는 경우에도 동일하게 동작합니다.

```
use App\Models\Order;

$order = Order::find(1);

$order->delete();
```

<!-- If you do not want to retrieve the model before deleting the record, you may use the `unsearchable` method on an Eloquent query instance: -->
모델을 먼저 조회하지 않고 바로 삭제하고 싶을 때는, Eloquent 쿼리 인스턴스에서 `unsearchable` 메서드를 사용할 수 있습니다.

```
Order::where('price', '>', 100)->unsearchable();
```

<!-- If you would like to remove the search index records for all of the models in a relationship, you may invoke the `unsearchable` on the relationship instance: -->
연관관계의 모든 모델 인스턴스를 인덱스에서 제거하려면, 연관관계 인스턴스에 `unsearchable`을 호출합니다.

```
$user->orders()->unsearchable();
```

<!-- Or, if you already have a collection of Eloquent models in memory, you may call the `unsearchable` method on the collection instance to remove the model instances from their corresponding index: -->
이미 모델 컬렉션이 있을 때는, 컬렉션 인스턴스에 `unsearchable`을 호출해 해당 모델들을 인덱스에서 제거할 수 있습니다.

```
$orders->unsearchable();
```

<a name="pausing-indexing"></a>
<!-- ### Pausing Indexing -->
### Pausing Indexing

<!-- Sometimes you may need to perform a batch of Eloquent operations on a model without syncing the model data to your search index. You may do this using the `withoutSyncingToSearch` method. This method accepts a single closure which will be immediately executed. Any model operations that occur within the closure will not be synced to the model's index: -->
여러 개의 Eloquent 모델을 한꺼번에 다뤄야 하지만, 이 동안에는 검색 인덱스와의 동기화를 일시적으로 중단하고 싶은 경우가 있습니다. 이런 경우에는 `withoutSyncingToSearch` 메서드를 사용하면 됩니다. 이 메서드는 하나의 클로저를 인자로 받으며, 클로저 내부에서 실행되는 모든 모델 동작은 인덱스에 반영되지 않습니다.

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
특정 조건에서만 모델을 검색 대상으로 만들고 싶은 경우가 있을 수 있습니다. 예를 들어, `App\Models\Post` 모델이 "초안(draft)" 또는 "공개(published)" 상태일 때, "공개" 상태일 때만 검색 가능하게 하고 싶다고 가정해봅시다. 이럴 때는 모델에 `shouldBeSearchable` 메서드를 정의하면 됩니다.

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
`shouldBeSearchable` 메서드는 `save`, `create` 메서드, 쿼리, 연관관계를 통해 모델을 처리할 때만 적용됩니다. 모델 인스턴스나 컬렉션에 직접 `searchable` 메서드를 호출하면, `shouldBeSearchable` 결과와 상관없이 인덱싱이 강제됩니다.

<a name="searching"></a>
<!-- ## Searching -->
## Searching

<!-- You may begin searching a model using the `search` method. The search method accepts a single string that will be used to search your models. You should then chain the `get` method onto the search query to retrieve the Eloquent models that match the given search query: -->
모델 검색은 `search` 메서드로 시작할 수 있습니다. 이 메서드는 하나의 문자열을 입력받아 해당 문자열이 포함된 모델을 검색합니다. 이후, `get` 메서드를 체이닝하여 원하는 검색 쿼리의 Eloquent 모델을 반환받을 수 있습니다.

```
use App\Models\Order;

$orders = Order::search('Star Trek')->get();
```

<!-- Since Scout searches return a collection of Eloquent models, you may even return the results directly from a route or controller and they will automatically be converted to JSON: -->
Scout의 검색 결과는 Eloquent 모델 컬렉션으로 반환되어 별도의 처리 없이 바로 JSON으로 변환해 라우트나 컨트롤러에서 직접 반환할 수 있습니다.

```
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/search', function (Request $request) {
    return Order::search($request->search)->get();
});
```

<!-- If you would like to get the raw search results before they are converted to Eloquent models, you may use the `raw` method: -->
검색 결과를 Eloquent 모델로 변환하기 전, 원시 검색 결과를 받아보고 싶다면 `raw` 메서드를 사용하면 됩니다.

```
$orders = Order::search('Star Trek')->raw();
```

<a name="custom-indexes"></a>
<!-- #### Custom Indexes -->
#### Custom Indexes

<!-- Search queries will typically be performed on the index specified by the model's [`searchableAs`](#configuring-model-indexes) method. However, you may use the `within` method to specify a custom index that should be searched instead: -->
검색 쿼리는 기본적으로 모델의 [`searchableAs`](#configuring-model-indexes) 메서드에서 지정한 인덱스를 대상으로 수행됩니다. 하지만, `within` 메서드를 사용하면 특정 커스텀 인덱스에서 검색하도록 할 수 있습니다.

```
$orders = Order::search('Star Trek')
    ->within('tv_shows_popularity_desc')
    ->get();
```

<a name="where-clauses"></a>
<!-- ### Where Clauses -->
### Where Clauses

<!-- Scout allows you to add simple "where" clauses to your search queries. Currently, these clauses only support basic numeric equality checks and are primarily useful for scoping search queries by an owner ID: -->
Scout는 간단한 "where" 조건을 검색 쿼리에 추가할 수 있습니다. 현재로서는 기본적인 숫자 동등 비교만 지원하며, 주로 owner ID처럼 특정 column에 범위를 한정해 검색할 때 유용합니다.

```
use App\Models\Order;

$orders = Order::search('Star Trek')->where('user_id', 1)->get();
```

<!-- You may use the `whereIn` method to constrain results against a given set of values: -->
`whereIn` 메서드를 사용하면 특정 값 집합을 기준으로 결과를 제한할 수 있습니다.

```
$orders = Order::search('Star Trek')->whereIn(
    'status', ['paid', 'open']
)->get();
```

<!-- Since a search index is not a relational database, more advanced "where" clauses are not currently supported. -->
검색 인덱스는 관계형 데이터베이스가 아니므로, 이 외의 복잡한 where 조건문은 현재 지원하지 않습니다.

<a name="pagination"></a>
<!-- ### Pagination -->
### Pagination

<!-- In addition to retrieving a collection of models, you may paginate your search results using the `paginate` method. This method will return an `Illuminate\Pagination\LengthAwarePaginator` instance just as if you had [paginated a traditional Eloquent query](/docs/8.x/pagination): -->
모델의 컬렉션을 단순히 반환하는 것 외에도, `paginate` 메서드로 검색 결과를 페이지네이션할 수 있습니다. 이 메서드는 [paginated a traditional Eloquent query](/docs/8.x/pagination)할 때와 마찬가지로 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 반환합니다.

```
use App\Models\Order;

$orders = Order::search('Star Trek')->paginate();
```

<!-- You may specify how many models to retrieve per page by passing the amount as the first argument to the `paginate` method: -->
한 페이지에 가져올 모델 개수를 지정하려면, `paginate` 메서드의 첫 번째 인자로 개수를 전달하면 됩니다.

```
$orders = Order::search('Star Trek')->paginate(15);
```

<!-- Once you have retrieved the results, you may display the results and render the page links using [Blade](/docs/8.x/blade) just as if you had paginated a traditional Eloquent query: -->
검색 결과를 가져온 뒤에는 [Blade](/docs/8.x/blade)에서 일반 페이지네이션 쿼리와 동일하게 내용을 표시하고 페이지 링크를 그릴 수 있습니다.

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

<!-- Of course, if you would like to retrieve the pagination results as JSON, you may return the paginator instance directly from a route or controller: -->
당연히, 페이지네이터 인스턴스를 라우트나 컨트롤러에서 바로 반환하면 결과를 JSON으로 받을 수도 있습니다.

```
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    return Order::search($request->input('query'))->paginate(15);
});
```

<a name="soft-deleting"></a>
<!-- ### Soft Deleting -->
### Soft Deleting

<!-- If your indexed models are [soft deleting](/docs/8.x/eloquent#soft-deleting) and you need to search your soft deleted models, set the `soft_delete` option of the `config/scout.php` configuration file to `true`: -->
인덱싱된 모델이 [soft deleting](/docs/8.x/eloquent#soft-deleting)를 사용하는 경우, 소프트 삭제된 모델도 검색하고 싶다면 `config/scout.php` 설정 파일의 `soft_delete` 옵션을 `true`로 설정하세요.

```
'soft_delete' => true,
```

<!-- When this configuration option is `true`, Scout will not remove soft deleted models from the search index. Instead, it will set a hidden `__soft_deleted` attribute on the indexed record. Then, you may use the `withTrashed` or `onlyTrashed` methods to retrieve the soft deleted records when searching: -->
이 설정이 `true`면, Scout는 소프트 삭제된 모델을 검색 인덱스에서 제거하지 않고, 인덱스에 숨겨진 `__soft_deleted` 속성을 추가합니다. 그리고 검색할 때는 `withTrashed` 또는 `onlyTrashed` 메서드를 사용해 소프트 삭제된 데이터도 함께 조회할 수 있습니다.

```
use App\Models\Order;

// Include trashed records when retrieving results...
$orders = Order::search('Star Trek')->withTrashed()->get();

// Only include trashed records when retrieving results...
$orders = Order::search('Star Trek')->onlyTrashed()->get();
```

> [!TIP]
> 소프트 삭제된 모델을 `forceDelete`로 완전히 삭제하면 Scout가 자동으로 인덱스에서 제거합니다.

<a name="customizing-engine-searches"></a>
<!-- ### Customizing Engine Searches -->
### Customizing Engine Searches

<!-- If you need to perform advanced customization of the search behavior of an engine you may pass a closure as the second argument to the `search` method. For example, you could use this callback to add geo-location data to your search options before the search query is passed to Algolia: -->
엔진의 검색 동작을 더 세밀하게 커스터마이징해야 할 경우, `search` 메서드의 두 번째 인자로 클로저를 전달할 수 있습니다. 예를 들어, 이 콜백을 이용해 검색 쿼리 옵션에 지리 데이터(geo-location)를 추가해서 Algolia에 넘길 수 있습니다.

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

<a name="custom-engines"></a>
<!-- ## Custom Engines -->
## Custom Engines

<a name="writing-the-engine"></a>
<!-- #### Writing The Engine -->
#### Writing The Engine

<!-- If one of the built-in Scout search engines doesn't fit your needs, you may write your own custom engine and register it with Scout. Your engine should extend the `Laravel\Scout\Engines\Engine` abstract class. This abstract class contains eight methods your custom engine must implement: -->
기본 제공되는 Scout 검색 엔진이 요구 사항에 맞지 않는 경우, 자신만의 커스텀 엔진을 작성해 Scout에 등록할 수 있습니다. 커스텀 엔진은 `Laravel\Scout\Engines\Engine` 추상 클래스를 상속해야 하며, 다음의 8가지 메서드를 반드시 구현해야 합니다.

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
이 메서드들의 구체적인 구현은 `Laravel\Scout\Engines\AlgoliaEngine` 클래스의 예시 코드를 참고하면 도움이 될 수 있습니다. 각 메서드가 실제로 어떻게 동작해야 하는지 참고하는 데 좋은 출발점이 됩니다.

<a name="registering-the-engine"></a>
<!-- #### Registering The Engine -->
#### Registering The Engine

<!-- Once you have written your custom engine, you may register it with Scout using the `extend` method of the Scout engine manager. Scout's engine manager may be resolved from the Laravel service container. You should call the `extend` method from the `boot` method of your `App\Providers\AppServiceProvider` class or any other service provider used by your application: -->
커스텀 엔진을 모두 구현했다면, Scout 엔진 매니저의 `extend` 메서드로 Scout에 등록할 수 있습니다. 엔진 매니저는 Laravel 서비스 컨테이너에서 resolve할 수 있습니다. 보통 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드나, 애플리케이션에서 사용하는 다른 서비스 프로바이더에서 `extend`를 호출합니다.

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
엔진 등록이 완료되면, `config/scout.php` 설정 파일에서 기본 Scout `driver`로 지정할 수 있습니다.

```
'driver' => 'mysql',
```

<a name="builder-macros"></a>
<!-- ## Builder Macros -->
## Builder Macros

<!-- If you would like to define a custom Scout search builder method, you may use the `macro` method on the `Laravel\Scout\Builder` class. Typically, "macros" should be defined within a [service provider's](/docs/8.x/providers) `boot` method: -->
Scout의 검색 빌더에 커스텀 메서드를 정의하고 싶다면, `Laravel\Scout\Builder` 클래스의 `macro` 메서드를 사용할 수 있습니다. 매크로는 주로 [service provider's](/docs/8.x/providers)의 `boot` 메서드에서 정의합니다.

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
`macro` 함수는 첫 번째 인자로 매크로 이름, 두 번째 인자로 클로저를 받습니다. 이후 정의한 매크로 이름을 `Laravel\Scout\Builder` 구현체에서 호출하면, 해당 클로저가 실행됩니다.

```
use App\Models\Order;

Order::search('Star Trek')->count();
```
