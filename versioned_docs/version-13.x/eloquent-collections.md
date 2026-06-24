<!-- # Eloquent: Collections -->
# Eloquent: Collections

- [Introduction](#introduction)
- [Available Methods](#available-methods)
- [Custom Collections](#custom-collections)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- All Eloquent methods that return more than one model result will return instances of the `Illuminate\Database\Eloquent\Collection` class, including results retrieved via the `get` method or accessed via a relationship. The Eloquent collection object extends Laravel's [base collection](/docs/13.x/collections), so it naturally inherits dozens of methods used to fluently work with the underlying array of Eloquent models. Be sure to review the Laravel collection documentation to learn all about these helpful methods! -->
둘 이상의 모델 결과를 반환하는 모든 Eloquent 메서드는 `get` 메서드를 통해 검색되거나 관계를 통해 액세스되는 결과를 포함하여 `Illuminate\Database\Eloquent\Collection` 클래스의 인스턴스를 반환합니다. Eloquent 컬렉션 개체는 Laravel의 [base collection](/docs/13.x/collections)을 확장하므로 Eloquent 모델의 기본 배열을 원활하게 작업하는 데 사용되는 수십 가지 메서드를 자연스럽게 상속합니다. 이러한 유용한 방법에 대한 모든 내용을 알아보려면 Laravel 컬렉션 문서를 검토하세요!

<!-- All collections also serve as iterators, allowing you to loop over them as if they were simple PHP arrays: -->
모든 컬렉션은 반복자 역할도 하므로 단순한 PHP 배열인 것처럼 반복할 수 있습니다.

```php
use App\Models\User;

$users = User::where('active', 1)->get();

foreach ($users as $user) {
    echo $user->name;
}
```

<!-- However, as previously mentioned, collections are much more powerful than arrays and expose a variety of map / reduce operations that may be chained using an intuitive interface. For example, we may remove all inactive models and then gather the first name for each remaining user: -->
그러나 앞서 언급했듯이 컬렉션은 배열보다 훨씬 강력하며 직관적인 인터페이스를 사용하여 연결될 수 있는 다양한 맵/리듀스 작업을 제공합니다. 예를 들어, 모든 비활성 모델을 제거한 다음 나머지 각 사용자의 이름을 수집할 수 있습니다.

```php
$names = User::all()->reject(function (User $user) {
    return $user->active === false;
})->map(function (User $user) {
    return $user->name;
});
```

<a name="eloquent-collection-conversion"></a>
<!-- #### Eloquent Collection Conversion -->
#### Eloquent Collection Conversion

<!-- While most Eloquent collection methods return a new instance of an Eloquent collection, the `collapse`, `flatten`, `flip`, `keys`, `pluck`, and `zip` methods return a [base collection](/docs/13.x/collections) instance. Likewise, if a `map` operation returns a collection that does not contain any Eloquent models, it will be converted to a base collection instance. -->
대부분의 Eloquent 컬렉션 메서드는 Eloquent 컬렉션의 새 인스턴스를 반환하지만, `collapse`, `flatten`, `flip`, `keys`, `pluck` 및 `zip` 메서드는 [base collection](/docs/13.x/collections) 인스턴스를 반환합니다. 마찬가지로, `map` 작업이 Eloquent 모델을 포함하지 않는 컬렉션을 반환하는 경우 기본 컬렉션 인스턴스로 변환됩니다.

<a name="available-methods"></a>
<!-- ## Available Methods -->
## Available Methods

<!-- All Eloquent collections extend the base [Laravel collection](/docs/13.x/collections#available-methods) object; therefore, they inherit all of the powerful methods provided by the base collection class. -->
모든 Eloquent 컬렉션은 기본 [Laravel collection](/docs/13.x/collections#available-methods) 개체를 확장합니다. 따라서 기본 컬렉션 클래스에서 제공하는 강력한 메서드를 모두 상속합니다.

<!-- In addition, the `Illuminate\Database\Eloquent\Collection` class provides a superset of methods to aid with managing your model collections. Most methods return `Illuminate\Database\Eloquent\Collection` instances; however, some methods, like `modelKeys`, return an `Illuminate\Support\Collection` instance. -->
또한 `Illuminate\Database\Eloquent\Collection` 클래스는 모델 컬렉션 관리에 도움이 되는 메서드의 상위 집합을 제공합니다. 대부분의 메소드는 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환합니다. 그러나 `modelKeys`와 같은 일부 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환합니다.

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[append](#method-append)
[contains](#method-contains)
[diff](#method-diff)
[except](#method-except)
[find](#method-find)
[findOrFail](#method-find-or-fail)
[fresh](#method-fresh)
[intersect](#method-intersect)
[load](#method-load)
[loadMissing](#method-loadMissing)
[modelKeys](#method-modelKeys)
[makeVisible](#method-makeVisible)
[makeHidden](#method-makeHidden)
[mergeVisible](#method-mergeVisible)
[mergeHidden](#method-mergeHidden)
[only](#method-only)
[partition](#method-partition)
[setAppends](#method-setAppends)
[setVisible](#method-setVisible)
[setHidden](#method-setHidden)
[toQuery](#method-toquery)
[unique](#method-unique)
[withoutAppends](#method-withoutAppends)
-->
[append](#method-append)
[contains](#method-contains)
[diff](#method-diff)
[except](#method-except)
[find](#method-find)
[findOrFail](#method-find-or-fail)
[fresh](#method-fresh)
[intersect](#method-intersect)
[load](#method-load)
[loadMissing](#method-loadMissing)
[modelKeys](#method-modelKeys)
[makeVisible](#method-makeVisible)
[makeHidden](#method-makeHidden)
[mergeVisible](#method-mergeVisible)
[mergeHidden](#method-mergeHidden)
[only](#method-only)
[partition](#method-partition)
[setAppends](#method-setAppends)
[setVisible](#method-setVisible)
[setHidden](#method-setHidden)
[toQuery](#method-toquery)
[unique](#method-unique)
[withoutAppends](#method-withoutAppends)

<!-- </div> -->
</div>

<a name="method-append"></a>
<!-- #### `append($attributes)` -->
#### `append($attributes)`

<!-- The `append` method may be used to indicate that an attribute should be [appended](/docs/13.x/eloquent-serialization#appending-values-to-json) for every model in the collection. This method accepts an array of attributes or a single attribute: -->
`append` 메소드는 컬렉션의 모든 모델에 대해 속성이 [appended](/docs/13.x/eloquent-serialization#appending-values-to-json)되어야 함을 나타내는 데 사용될 수 있습니다. 이 메소드는 속성 배열 또는 단일 속성을 허용합니다.

```php
$users->append('team');

$users->append(['team', 'is_admin']);
```

<a name="method-contains"></a>
<!-- #### `contains($key, $operator = null, $value = null)` -->
#### `contains($key, $operator = null, $value = null)`

<!-- The `contains` method may be used to determine if a given model instance is contained by the collection. This method accepts a primary key or a model instance: -->
`contains` 메소드는 주어진 모델 인스턴스가 컬렉션에 포함되어 있는지 확인하는 데 사용될 수 있습니다. 이 메서드는 기본 키 또는 모델 인스턴스를 허용합니다.

```php
$users->contains(1);

$users->contains(User::find(1));
```

<a name="method-diff"></a>
<!-- #### `diff($items)` -->
#### `diff($items)`

<!-- The `diff` method returns all of the models that are not present in the given collection: -->
`diff` 메소드는 지정된 컬렉션에 없는 모든 모델을 반환합니다.

```php
use App\Models\User;

$users = $users->diff(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-except"></a>
<!-- #### `except($keys)` -->
#### `except($keys)`

<!-- The `except` method returns all of the models that do not have the given primary keys: -->
`except` 메소드는 지정된 기본 키가 없는 모든 모델을 반환합니다.

```php
$users = $users->except([1, 2, 3]);
```

<a name="method-find"></a>
<!-- #### `find($key)` -->
#### `find($key)`

<!-- The `find` method returns the model that has a primary key matching the given key. If `$key` is a model instance, `find` will attempt to return a model matching the primary key. If `$key` is an array of keys, `find` will return all models which have a primary key in the given array: -->
`find` 메소드는 지정된 키와 일치하는 기본 키가 있는 모델을 반환합니다. `$key`가 모델 인스턴스인 경우 `find`는 기본 키와 일치하는 모델을 반환하려고 시도합니다. `$key`가 키 배열인 경우 `find`는 지정된 배열에 기본 키가 있는 모든 모델을 반환합니다.

```php
$users = User::all();

$user = $users->find(1);
```

<a name="method-find-or-fail"></a>
<!-- #### `findOrFail($key)` -->
#### `findOrFail($key)`

<!-- The `findOrFail` method returns the model that has a primary key matching the given key or throws an `Illuminate\Database\Eloquent\ModelNotFoundException` exception if no matching model can be found in the collection: -->
`findOrFail` 메소드는 지정된 키와 일치하는 기본 키가 있는 모델을 반환하거나 컬렉션에서 일치하는 모델을 찾을 수 없는 경우 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 발생시킵니다.

```php
$users = User::all();

$user = $users->findOrFail(1);
```

<a name="method-fresh"></a>
<!-- #### `fresh($with = [])` -->
#### `fresh($with = [])`

<!-- The `fresh` method retrieves a fresh instance of each model in the collection from the database. In addition, any specified relationships will be eager loaded: -->
`fresh` 메서드는 데이터베이스에서 컬렉션에 있는 각 모델의 새 인스턴스를 검색합니다. 또한 지정된 관계가 모두 즉시 로드됩니다.

```php
$users = $users->fresh();

$users = $users->fresh('comments');
```

<a name="method-intersect"></a>
<!-- #### `intersect($items)` -->
#### `intersect($items)`

<!-- The `intersect` method returns all of the models that are also present in the given collection: -->
`intersect` 메소드는 지정된 컬렉션에도 존재하는 모든 모델을 반환합니다.

```php
use App\Models\User;

$users = $users->intersect(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-load"></a>
<!-- #### `load($relations)` -->
#### `load($relations)`

<!-- The `load` method eager loads the given relationships for all models in the collection: -->
`load` 메소드는 컬렉션의 모든 모델에 대해 지정된 관계를 로드합니다.

```php
$users->load(['comments', 'posts']);

$users->load('comments.author');

$users->load(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-loadMissing"></a>
<!-- #### `loadMissing($relations)` -->
#### `loadMissing($relations)`

<!-- The `loadMissing` method eager loads the given relationships for all models in the collection if the relationships are not already loaded: -->
`loadMissing` 메소드는 관계가 아직 로드되지 않은 경우 컬렉션의 모든 모델에 대해 지정된 관계를 로드합니다.

```php
$users->loadMissing(['comments', 'posts']);

$users->loadMissing('comments.author');

$users->loadMissing(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-modelKeys"></a>
<!-- #### `modelKeys()` -->
#### `modelKeys()`

<!-- The `modelKeys` method returns the primary keys for all models in the collection: -->
`modelKeys` 메서드는 컬렉션의 모든 모델에 대한 기본 키를 반환합니다.

```php
$users->modelKeys();

// [1, 2, 3, 4, 5]
```

<a name="method-makeVisible"></a>
<!-- #### `makeVisible($attributes)` -->
#### `makeVisible($attributes)`

<!-- The `makeVisible` method [makes attributes visible](/docs/13.x/eloquent-serialization#hiding-attributes-from-json) that are typically "hidden" on each model in the collection: -->
`makeVisible` 메서드는 일반적으로 컬렉션의 각 모델에 "숨겨진" [makes attributes visible](/docs/13.x/eloquent-serialization#hiding-attributes-from-json)합니다.

```php
$users = $users->makeVisible(['address', 'phone_number']);
```

<a name="method-makeHidden"></a>
<!-- #### `makeHidden($attributes)` -->
#### `makeHidden($attributes)`

<!-- The `makeHidden` method [hides attributes](/docs/13.x/eloquent-serialization#hiding-attributes-from-json) that are typically "visible" on each model in the collection: -->
`makeHidden` 메서드는 컬렉션의 각 모델에서 일반적으로 "표시"되는 [hides attributes](/docs/13.x/eloquent-serialization#hiding-attributes-from-json):

```php
$users = $users->makeHidden(['address', 'phone_number']);
```

<a name="method-mergeVisible"></a>
<!-- #### `mergeVisible($attributes)` -->
#### `mergeVisible($attributes)`

<!-- The `mergeVisible` method [makes additional attributes visible](/docs/13.x/eloquent-serialization#hiding-attributes-from-json) while retaining existing visible attributes: -->
`mergeVisible` 메소드는 기존 가시 속성을 유지하면서 [makes additional attributes visible](/docs/13.x/eloquent-serialization#hiding-attributes-from-json)합니다.

```php
$users = $users->mergeVisible(['middle_name']);
```

<a name="method-mergeHidden"></a>
<!-- #### `mergeHidden($attributes)` -->
#### `mergeHidden($attributes)`

<!-- The `mergeHidden` method [hides additional attributes](/docs/13.x/eloquent-serialization#hiding-attributes-from-json) while retaining existing hidden attributes: -->
`mergeHidden` 방법은 기존 숨겨진 속성을 유지하면서 [hides additional attributes](/docs/13.x/eloquent-serialization#hiding-attributes-from-json):

```php
$users = $users->mergeHidden(['last_login_at']);
```

<a name="method-only"></a>
<!-- #### `only($keys)` -->
#### `only($keys)`

<!-- The `only` method returns all of the models that have the given primary keys: -->
`only` 메소드는 지정된 기본 키가 있는 모든 모델을 반환합니다.

```php
$users = $users->only([1, 2, 3]);
```

<a name="method-partition"></a>
<!-- #### `partition` -->
#### `partition`

<!-- The `partition` method returns an instance of `Illuminate\Support\Collection` containing `Illuminate\Database\Eloquent\Collection` collection instances: -->
`partition` 메소드는 `Illuminate\Database\Eloquent\Collection` 컬렉션 인스턴스를 포함하는 `Illuminate\Support\Collection` 인스턴스를 반환합니다.

```php
$partition = $users->partition(fn ($user) => $user->age > 18);

dump($partition::class);    // Illuminate\Support\Collection
dump($partition[0]::class); // Illuminate\Database\Eloquent\Collection
dump($partition[1]::class); // Illuminate\Database\Eloquent\Collection
```

<a name="method-setAppends"></a>
<!-- #### `setAppends($attributes)` -->
#### `setAppends($attributes)`

<!-- The `setAppends` method temporarily overrides all of the [appended attributes](/docs/13.x/eloquent-serialization#appending-values-to-json) on each model in the collection: -->
`setAppends` 메서드는 컬렉션의 각 모델에 대한 모든 [appended attributes](/docs/13.x/eloquent-serialization#appending-values-to-json)을 일시적으로 재정의합니다.

```php
$users = $users->setAppends(['is_admin']);
```

<a name="method-setVisible"></a>
<!-- #### `setVisible($attributes)` -->
#### `setVisible($attributes)`

<!-- The `setVisible` method [temporarily overrides](/docs/13.x/eloquent-serialization#temporarily-modifying-attribute-visibility) all of the visible attributes on each model in the collection: -->
`setVisible` 메서드는 컬렉션의 각 모델에 표시되는 모든 속성을 [temporarily overrides](/docs/13.x/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다.

```php
$users = $users->setVisible(['id', 'name']);
```

<a name="method-setHidden"></a>
<!-- #### `setHidden($attributes)` -->
#### `setHidden($attributes)`

<!-- The `setHidden` method [temporarily overrides](/docs/13.x/eloquent-serialization#temporarily-modifying-attribute-visibility) all of the hidden attributes on each model in the collection: -->
`setHidden` 메서드는 컬렉션의 각 모델에 대한 모든 숨겨진 속성을 [temporarily overrides](/docs/13.x/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다.

```php
$users = $users->setHidden(['email', 'password', 'remember_token']);
```

<a name="method-toquery"></a>
<!-- #### `toQuery()` -->
#### `toQuery()`

<!-- The `toQuery` method returns an Eloquent query builder instance containing a `whereIn` constraint on the collection model's primary keys: -->
`toQuery` 메소드는 컬렉션 모델의 기본 키에 대한 `whereIn` 제약 조건을 포함하는 Eloquent 쿼리 빌더 인스턴스를 반환합니다.

```php
use App\Models\User;

$users = User::where('status', 'VIP')->get();

$users->toQuery()->update([
    'status' => 'Administrator',
]);
```

<a name="method-unique"></a>
<!-- #### `unique($key = null, $strict = false)` -->
#### `unique($key = null, $strict = false)`

<!-- The `unique` method returns all of the unique models in the collection. Any models with the same primary key as another model in the collection are removed: -->
`unique` 메서드는 컬렉션의 고유한 모델을 모두 반환합니다. 컬렉션의 다른 모델와 동일한 기본 키를 가진 모든 모델이 제거됩니다.

```php
$users = $users->unique();
```

<a name="method-withoutAppends"></a>
<!-- #### `withoutAppends()` -->
#### `withoutAppends()`

<!-- The `withoutAppends` method temporarily removes all of the [appended attributes](/docs/13.x/eloquent-serialization#appending-values-to-json) on each model in the collection: -->
`withoutAppends` 메서드는 컬렉션의 각 모델에서 모든 [appended attributes](/docs/13.x/eloquent-serialization#appending-values-to-json)을 일시적으로 제거합니다.

```php
$users = $users->withoutAppends();
```

<a name="custom-collections"></a>
<!-- ## Custom Collections -->
## Custom Collections

<!-- If you would like to use a custom `Collection` object when interacting with a given model, you may add the `CollectedBy` attribute to your model: -->
특정 모델와 상호작용할 때 사용자 지정 `Collection` 개체를 사용하려면 모델에 `CollectedBy` 속성을 추가하면 됩니다.

```php
<?php

namespace App\Models;

use App\Support\UserCollection;
use Illuminate\Database\Eloquent\Attributes\CollectedBy;
use Illuminate\Database\Eloquent\Model;

#[CollectedBy(UserCollection::class)]
class User extends Model
{
    // ...
}
```

<!-- Alternatively, you may define a `newCollection` method on your model: -->
또는 모델에 `newCollection` 메서드를 정의할 수도 있습니다.

```php
<?php

namespace App\Models;

use App\Support\UserCollection;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Create a new Eloquent Collection instance.
     *
     * @param  array<int, \Illuminate\Database\Eloquent\Model>  $models
     * @return \Illuminate\Database\Eloquent\Collection<int, \Illuminate\Database\Eloquent\Model>
     */
    public function newCollection(array $models = []): Collection
    {
        $collection = new UserCollection($models);

        if (Model::isAutomaticallyEagerLoadingRelationships()) {
            $collection->withRelationshipAutoloading();
        }

        return $collection;
    }
}
```

<!-- Once you have defined a `newCollection` method or added the `CollectedBy` attribute to your model, you will receive an instance of your custom collection anytime Eloquent would normally return an `Illuminate\Database\Eloquent\Collection` instance. -->
`newCollection` 메서드를 정의하거나 모델에 `CollectedBy` 속성을 추가하면 Eloquent가 일반적으로 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환할 때마다 사용자 지정 컬렉션의 인스턴스를 받게 됩니다.

<!-- If you would like to use a custom collection for every model in your application, you should define the `newCollection` method on a base model class that is extended by all of your application's models. -->
애플리케이션의 모든 모델에 대해 사용자 지정 컬렉션을 사용하려면 애플리케이션의 모든 모델에 의해 확장되는 기본 모델 클래스에 `newCollection` 메서드를 정의해야 합니다.
