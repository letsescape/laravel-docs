<!-- # Eloquent: Collections -->
# Eloquent: Collections

- [Introduction](#introduction)
- [Available Methods](#available-methods)
- [Custom Collections](#custom-collections)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- All Eloquent methods that return more than one model result will return instances of the `Illuminate\Database\Eloquent\Collection` class, including results retrieved via the `get` method or accessed via a relationship. The Eloquent collection object extends Laravel's [base collection](/docs/8.x/collections), so it naturally inherits dozens of methods used to fluently work with the underlying array of Eloquent models. Be sure to review the Laravel collection documentation to learn all about these helpful methods! -->
여러 개의 모델 결과를 반환하는 모든 Eloquent 메서드는 `get` 메서드로 데이터를 조회할 때나, 관계를 통해 접근할 때와 같이 항상 `Illuminate\Database\Eloquent\Collection` 클래스의 인스턴스를 반환합니다. 이 Eloquent 컬렉션 객체는 Laravel의 [base collection](/docs/8.x/collections)을 확장하고 있으므로, Eloquent 모델로 이루어진 내부 배열을 유연하게 다룰 수 있는 다양한 메서드를 그대로 사용할 수 있습니다. 이 유용한 메서드들에 대해서는 Laravel 컬렉션 공식 문서를 꼭 참고해보시기 바랍니다.

<!-- All collections also serve as iterators, allowing you to loop over them as if they were simple PHP arrays: -->
Eloquent 컬렉션도 반복자(iterator)이기 때문에, 간단한 PHP 배열처럼 컬렉션을 순회할 수도 있습니다:

```
use App\Models\User;

$users = User::where('active', 1)->get();

foreach ($users as $user) {
    echo $user->name;
}
```

<!-- However, as previously mentioned, collections are much more powerful than arrays and expose a variety of map / reduce operations that may be chained using an intuitive interface. For example, we may remove all inactive models and then gather the first name for each remaining user: -->
하지만 앞서 언급한 것처럼, 컬렉션은 배열보다 훨씬 강력하며, 직관적인 인터페이스를 통해 다양한 map/reduce(배열 변환/축소) 연산을 체이닝 방식으로 사용할 수 있습니다. 예를 들어, 아래 예시처럼 비활성화된 모델은 모두 제외하고 남은 유저들의 이름만 모을 수도 있습니다.

```
$names = User::all()->reject(function ($user) {
    return $user->active === false;
})->map(function ($user) {
    return $user->name;
});
```

<a name="eloquent-collection-conversion"></a>
<!-- #### Eloquent Collection Conversion -->
#### Eloquent Collection Conversion

<!-- While most Eloquent collection methods return a new instance of an Eloquent collection, the `collapse`, `flatten`, `flip`, `keys`, `pluck`, and `zip` methods return a [base collection](/docs/8.x/collections) instance. Likewise, if a `map` operation returns a collection that does not contain any Eloquent models, it will be converted to a base collection instance. -->
대부분의 Eloquent 컬렉션 메서드는 새로운 Eloquent 컬렉션 인스턴스를 반환하지만, `collapse`, `flatten`, `flip`, `keys`, `pluck`, `zip` 메서드는 [base collection](/docs/8.x/collections) 인스턴스를 반환합니다. 비슷하게, `map` 연산 결과에 Eloquent 모델이 하나도 없다면, 결과가 기본 컬렉션 인스턴스로 변환됩니다.

<a name="available-methods"></a>
<!-- ## Available Methods -->
## Available Methods

<!-- All Eloquent collections extend the base [Laravel collection](/docs/8.x/collections#available-methods) object; therefore, they inherit all of the powerful methods provided by the base collection class. -->
모든 Eloquent 컬렉션은 기본 [Laravel collection](/docs/8.x/collections#available-methods) 객체를 확장하므로, 기본 컬렉션 클래스에서 제공하는 강력한 메서드들을 그대로 사용할 수 있습니다.

<!-- In addition, the `Illuminate\Database\Eloquent\Collection` class provides a superset of methods to aid with managing your model collections. Most methods return `Illuminate\Database\Eloquent\Collection` instances; however, some methods, like `modelKeys`, return an `Illuminate\Support\Collection` instance. -->
추가로, `Illuminate\Database\Eloquent\Collection` 클래스는 모델 컬렉션을 편리하게 다룰 수 있도록 몇 가지 확장 메서드도 제공합니다. 대부분의 메서드는 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하지만, `modelKeys`와 같은 일부 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환합니다.



<!-- <div id="collection-method-list" markdown="1"> -->
<div id="collection-method-list" markdown="1">

<!--
[contains](#method-contains)
[diff](#method-diff)
[except](#method-except)
[find](#method-find)
[fresh](#method-fresh)
[intersect](#method-intersect)
[load](#method-load)
[loadMissing](#method-loadMissing)
[modelKeys](#method-modelKeys)
[makeVisible](#method-makeVisible)
[makeHidden](#method-makeHidden)
[only](#method-only)
[toQuery](#method-toquery)
[unique](#method-unique)
-->
[contains](#method-contains)
[diff](#method-diff)
[except](#method-except)
[find](#method-find)
[fresh](#method-fresh)
[intersect](#method-intersect)
[load](#method-load)
[loadMissing](#method-loadMissing)
[modelKeys](#method-modelKeys)
[makeVisible](#method-makeVisible)
[makeHidden](#method-makeHidden)
[only](#method-only)
[toQuery](#method-toquery)
[unique](#method-unique)

<!-- </div> -->
</div>

<a name="method-contains"></a>
<!-- #### `contains($key, $operator = null, $value = null)` -->
#### `contains($key, $operator = null, $value = null)`

<!-- The `contains` method may be used to determine if a given model instance is contained by the collection. This method accepts a primary key or a model instance: -->
`contains` 메서드는 컬렉션에 특정 모델 인스턴스가 포함되어 있는지 확인할 수 있습니다. 이 메서드는 기본키 또는 모델 인스턴스를 인수로 받을 수 있습니다.

```
$users->contains(1);

$users->contains(User::find(1));
```

<a name="method-diff"></a>
<!-- #### `diff($items)` -->
#### `diff($items)`

<!-- The `diff` method returns all of the models that are not present in the given collection: -->
`diff` 메서드는 주어진 컬렉션에 없는 모든 모델들을 반환합니다.

```
use App\Models\User;

$users = $users->diff(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-except"></a>
<!-- #### `except($keys)` -->
#### `except($keys)`

<!-- The `except` method returns all of the models that do not have the given primary keys: -->
`except` 메서드는 주어진 기본키를 가진 모델을 제외한 나머지 모델들을 반환합니다.

```
$users = $users->except([1, 2, 3]);
```

<a name="method-find"></a>
<!-- #### `find($key)` -->
#### `find($key)`

<!-- The `find` method returns the model that has a primary key matching the given key. If `$key` is a model instance, `find` will attempt to return a model matching the primary key. If `$key` is an array of keys, `find` will return all models which have a primary key in the given array: -->
`find` 메서드는 인자로 전달된 값과 기본키가 일치하는 모델을 반환합니다. `$key`가 모델 인스턴스라면, `find`는 내부적으로 해당 기본키와 일치하는 모델을 반환합니다. `$key`가 키 값의 배열일 경우, `find`는 해당 배열에 포함된 기본키를 가진 모델들을 모두 반환합니다.

```
$users = User::all();

$user = $users->find(1);
```

<a name="method-fresh"></a>
<!-- #### `fresh($with = [])` -->
#### `fresh($with = [])`

<!-- The `fresh` method retrieves a fresh instance of each model in the collection from the database. In addition, any specified relationships will be eager loaded: -->
`fresh` 메서드는 컬렉션에 포함된 각 모델의 최신 데이터를 데이터베이스에서 새로 조회해 반환합니다. 추가로 특정 관계도 함께 eager load 할 수 있습니다.

```
$users = $users->fresh();

$users = $users->fresh('comments');
```

<a name="method-intersect"></a>
<!-- #### `intersect($items)` -->
#### `intersect($items)`

<!-- The `intersect` method returns all of the models that are also present in the given collection: -->
`intersect` 메서드는 주어진 컬렉션에도 존재하는 모델만 반환합니다.

```
use App\Models\User;

$users = $users->intersect(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-load"></a>
<!-- #### `load($relations)` -->
#### `load($relations)`

<!-- The `load` method eager loads the given relationships for all models in the collection: -->
`load` 메서드는 컬렉션의 모든 모델에서 지정한 관계를 eager load(즉시 로드)합니다.

```
$users->load(['comments', 'posts']);

$users->load('comments.author');
```

<a name="method-loadMissing"></a>
<!-- #### `loadMissing($relations)` -->
#### `loadMissing($relations)`

<!-- The `loadMissing` method eager loads the given relationships for all models in the collection if the relationships are not already loaded: -->
`loadMissing` 메서드는 컬렉션의 모든 모델에서 지정한 관계가 아직 로드되지 않았다면 eager load 합니다.

```
$users->loadMissing(['comments', 'posts']);

$users->loadMissing('comments.author');
```

<a name="method-modelKeys"></a>
<!-- #### `modelKeys()` -->
#### `modelKeys()`

<!-- The `modelKeys` method returns the primary keys for all models in the collection: -->
`modelKeys` 메서드는 컬렉션 내 모든 모델의 기본키(Primary Key)만 배열로 반환합니다.

```
$users->modelKeys();

// [1, 2, 3, 4, 5]
```

<a name="method-makeVisible"></a>
<!-- #### `makeVisible($attributes)` -->
#### `makeVisible($attributes)`

<!-- The `makeVisible` method [makes attributes visible](/docs/8.x/eloquent-serialization#hiding-attributes-from-json) that are typically "hidden" on each model in the collection: -->
`makeVisible` 메서드는 컬렉션 내 각 모델에서 평소 "숨겨진" 상태인 [makes attributes visible](/docs/8.x/eloquent-serialization#hiding-attributes-from-json)합니다.

```
$users = $users->makeVisible(['address', 'phone_number']);
```

<a name="method-makeHidden"></a>
<!-- #### `makeHidden($attributes)` -->
#### `makeHidden($attributes)`

<!-- The `makeHidden` method [hides attributes](/docs/8.x/eloquent-serialization#hiding-attributes-from-json) that are typically "visible" on each model in the collection: -->
`makeHidden` 메서드는 컬렉션 내 각 모델에서 평소 "보이는" 상태인 [hides attributes](/docs/8.x/eloquent-serialization#hiding-attributes-from-json)합니다.

```
$users = $users->makeHidden(['address', 'phone_number']);
```

<a name="method-only"></a>
<!-- #### `only($keys)` -->
#### `only($keys)`

<!-- The `only` method returns all of the models that have the given primary keys: -->
`only` 메서드는 전달받은 기본키를 가진 모델만을 남기고 반환합니다.

```
$users = $users->only([1, 2, 3]);
```

<a name="method-toquery"></a>
<!-- #### `toQuery()` -->
#### `toQuery()`

<!-- The `toQuery` method returns an Eloquent query builder instance containing a `whereIn` constraint on the collection model's primary keys: -->
`toQuery` 메서드는 컬렉션에 포함된 모델들의 기본키를 기준으로 `whereIn` 조건이 적용된 Eloquent 쿼리 빌더 인스턴스를 반환합니다.

```
use App\Models\User;

$users = User::where('status', 'VIP')->get();

$users->toQuery()->update([
    'status' => 'Administrator',
]);
```

<a name="method-unique"></a>
<!-- #### `unique($key = null, $strict = false)` -->
#### `unique($key = null, $strict = false)`

<!-- The `unique` method returns all of the unique models in the collection. Any models of the same type with the same primary key as another model in the collection are removed: -->
`unique` 메서드는 컬렉션 내에서 중복되는 모델을 제거하고, 고유한 모델만 반환합니다. 같은 타입의 모델 중 기본키가 동일한 경우 하나만 남게 됩니다.

```
$users = $users->unique();
```

<a name="custom-collections"></a>
<!-- ## Custom Collections -->
## Custom Collections

<!-- If you would like to use a custom `Collection` object when interacting with a given model, you may define a `newCollection` method on your model: -->
특정 모델에서 커스텀 `Collection` 객체를 사용하고 싶다면, 모델 클래스 안에 `newCollection` 메서드를 정의할 수 있습니다.

```
<?php

namespace App\Models;

use App\Support\UserCollection;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Create a new Eloquent Collection instance.
     *
     * @param  array  $models
     * @return \Illuminate\Database\Eloquent\Collection
     */
    public function newCollection(array $models = [])
    {
        return new UserCollection($models);
    }
}
```

<!-- Once you have defined a `newCollection` method, you will receive an instance of your custom collection anytime Eloquent would normally return an `Illuminate\Database\Eloquent\Collection` instance. If you would like to use a custom collection for every model in your application, you should define the `newCollection` method on a base model class that is extended by all of your application's models. -->
`newCollection` 메서드를 정의하면, 해당 모델에서 Eloquent가 원래 `Illuminate\Database\Eloquent\Collection`을 반환하는 모든 동작에서 이제 커스텀 컬렉션 인스턴스를 반환하게 됩니다. 만약 애플리케이션 내의 모든 모델에서 공통적으로 커스텀 컬렉션을 사용하고 싶다면, 각 모델이 상속받는 베이스 모델 클래스에 `newCollection` 메서드를 정의하면 됩니다.
