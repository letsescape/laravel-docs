<!-- # Eloquent: Collections -->
# Eloquent: Collections

- [Introduction](#introduction)
- [Available Methods](#available-methods)
- [Custom Collections](#custom-collections)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- All Eloquent methods that return more than one model result will return instances of the `Illuminate\Database\Eloquent\Collection` class, including results retrieved via the `get` method or accessed via a relationship. The Eloquent collection object extends Laravel's [base collection](/docs/11.x/collections), so it naturally inherits dozens of methods used to fluently work with the underlying array of Eloquent models. Be sure to review the Laravel collection documentation to learn all about these helpful methods! -->
Eloquent의 모든 메서드 중, 여러 개의 모델 결과를 반환하는 경우에는 항상 `Illuminate\Database\Eloquent\Collection` 클래스의 인스턴스를 반환합니다. 이는 `get` 메서드로 데이터를 조회하거나, 연관관계(relationship)를 통해 데이터를 가져오는 경우 모두 해당합니다. 이 Eloquent 컬렉션 객체는 Laravel의 [base collection](/docs/11.x/collections)을 확장하므로, Eloquent 모델 배열을 유연하게 다룰 수 있는 수십 가지 메서드를 자연스럽게 사용할 수 있습니다. 이 유용한 메서드들에 대해 더 자세히 알고 싶다면 Laravel 컬렉션 공식 문서를 반드시 참고하시기 바랍니다!

<!-- All collections also serve as iterators, allowing you to loop over them as if they were simple PHP arrays: -->
컬렉션은 또한 반복자(iterator) 역할을 하므로, 일반 PHP 배열처럼 손쉽게 반복문을 사용할 수 있습니다.

```
use App\Models\User;

$users = User::where('active', 1)->get();

foreach ($users as $user) {
    echo $user->name;
}
```

<!-- However, as previously mentioned, collections are much more powerful than arrays and expose a variety of map / reduce operations that may be chained using an intuitive interface. For example, we may remove all inactive models and then gather the first name for each remaining user: -->
하지만 앞에서 언급한 것처럼, 컬렉션은 단순한 배열보다 훨씬 강력합니다. 직관적인 인터페이스를 통해 다양한 map, reduce와 같은 연산을 체이닝하여 사용할 수 있습니다. 예를 들어, 비활성화된 모델을 필터링한 후, 각 사용자(user)의 이름만 추출하는 코드도 간단하게 작성할 수 있습니다.

```
$names = User::all()->reject(function (User $user) {
    return $user->active === false;
})->map(function (User $user) {
    return $user->name;
});
```

<a name="eloquent-collection-conversion"></a>
<!-- #### Eloquent Collection Conversion -->
#### Eloquent Collection Conversion

<!-- While most Eloquent collection methods return a new instance of an Eloquent collection, the `collapse`, `flatten`, `flip`, `keys`, `pluck`, and `zip` methods return a [base collection](/docs/11.x/collections) instance. Likewise, if a `map` operation returns a collection that does not contain any Eloquent models, it will be converted to a base collection instance. -->
대부분의 Eloquent 컬렉션 메서드는 항상 새로운 Eloquent 컬렉션 인스턴스를 반환합니다. 하지만 `collapse`, `flatten`, `flip`, `keys`, `pluck`, `zip` 같은 메서드는 [base collection](/docs/11.x/collections) 인스턴스를 반환합니다. 그리고 `map` 연산 결과가 Eloquent 모델이 아니라면, 해당 결과 컬렉션도 기본 컬렉션 인스턴스로 변환됩니다.

<a name="available-methods"></a>
<!-- ## Available Methods -->
## Available Methods

<!-- All Eloquent collections extend the base [Laravel collection](/docs/11.x/collections#available-methods) object; therefore, they inherit all of the powerful methods provided by the base collection class. -->
모든 Eloquent 컬렉션은 기본 [Laravel collection](/docs/11.x/collections#available-methods) 객체를 상속받기 때문에, 기본 컬렉션 클래스에서 제공하는 모든 강력한 메서드를 그대로 사용할 수 있습니다.

<!-- In addition, the `Illuminate\Database\Eloquent\Collection` class provides a superset of methods to aid with managing your model collections. Most methods return `Illuminate\Database\Eloquent\Collection` instances; however, some methods, like `modelKeys`, return an `Illuminate\Support\Collection` instance. -->
추가로, `Illuminate\Database\Eloquent\Collection` 클래스에는 모델 컬렉션을 더 효율적으로 다룰 수 있도록 돕는 여러 추가 메서드를 포함하고 있습니다. 대부분의 메서드는 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하지만, `modelKeys`와 같은 일부 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환하기도 합니다.



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
[only](#method-only)
[setVisible](#method-setVisible)
[setHidden](#method-setHidden)
[toQuery](#method-toquery)
[unique](#method-unique)
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
[only](#method-only)
[setVisible](#method-setVisible)
[setHidden](#method-setHidden)
[toQuery](#method-toquery)
[unique](#method-unique)

<!-- </div> -->
</div>

<a name="method-append"></a>
<!-- #### `append($attributes)` -->
#### `append($attributes)`

<!-- The `append` method may be used to indicate that an attribute should be [appended](/docs/11.x/eloquent-serialization#appending-values-to-json) for every model in the collection. This method accepts an array of attributes or a single attribute: -->
`append` 메서드는 컬렉션 내의 모든 모델에 대해 [appended](/docs/11.x/eloquent-serialization#appending-values-to-json)할 때 사용합니다. 이 메서드는 속성의 배열 또는 단일 속성을 인자로 받을 수 있습니다.

```
$users->append('team');

$users->append(['team', 'is_admin']);
```

<a name="method-contains"></a>
<!-- #### `contains($key, $operator = null, $value = null)` -->
#### `contains($key, $operator = null, $value = null)`

<!-- The `contains` method may be used to determine if a given model instance is contained by the collection. This method accepts a primary key or a model instance: -->
`contains` 메서드는 해당 컬렉션 안에 특정 모델 인스턴스가 포함되어 있는지 확인할 때 사용합니다. 이 메서드는 기본키 또는 모델 인스턴스를 인자로 받을 수 있습니다.

```
$users->contains(1);

$users->contains(User::find(1));
```

<a name="method-diff"></a>
<!-- #### `diff($items)` -->
#### `diff($items)`

<!-- The `diff` method returns all of the models that are not present in the given collection: -->
`diff` 메서드는 주어진 컬렉션에 없는 모델들만 결과로 반환합니다.

```
use App\Models\User;

$users = $users->diff(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-except"></a>
<!-- #### `except($keys)` -->
#### `except($keys)`

<!-- The `except` method returns all of the models that do not have the given primary keys: -->
`except` 메서드는 인자로 전달한 기본키(primary key)를 갖지 않은 모든 모델만을 반환합니다.

```
$users = $users->except([1, 2, 3]);
```

<a name="method-find"></a>
<!-- #### `find($key)` -->
#### `find($key)`

<!-- The `find` method returns the model that has a primary key matching the given key. If `$key` is a model instance, `find` will attempt to return a model matching the primary key. If `$key` is an array of keys, `find` will return all models which have a primary key in the given array: -->
`find` 메서드는 전달한 키와 일치하는 기본키(primary key)를 가진 모델을 반환합니다. `$key`가 모델 인스턴스인 경우에는 `find`가 해당 모델의 기본키와 같은 모델을 반환하려 시도합니다. `$key`가 키들의 배열이라면, `find`는 배열에 해당하는 모든 모델을 반환합니다.

```
$users = User::all();

$user = $users->find(1);
```

<a name="method-find-or-fail"></a>
<!-- #### `findOrFail($key)` -->
#### `findOrFail($key)`

<!-- The `findOrFail` method returns the model that has a primary key matching the given key or throws an `Illuminate\Database\Eloquent\ModelNotFoundException` exception if no matching model can be found in the collection: -->
`findOrFail` 메서드는 전달한 키와 일치하는 기본키를 가진 모델을 반환하며, 컬렉션에 일치하는 모델이 없으면 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 발생시킵니다.

```
$users = User::all();

$user = $users->findOrFail(1);
```

<a name="method-fresh"></a>
<!-- #### `fresh($with = [])` -->
#### `fresh($with = [])`

<!-- The `fresh` method retrieves a fresh instance of each model in the collection from the database. In addition, any specified relationships will be eager loaded: -->
`fresh` 메서드는 컬렉션의 모든 모델 인스턴스를 데이터베이스에서 새로 조회해 가져옵니다. 또한, 인자로 관계를 전달하면 해당 관계도 즉시 로드(eager load) 합니다.

```
$users = $users->fresh();

$users = $users->fresh('comments');
```

<a name="method-intersect"></a>
<!-- #### `intersect($items)` -->
#### `intersect($items)`

<!-- The `intersect` method returns all of the models that are also present in the given collection: -->
`intersect` 메서드는 주어진 컬렉션에 포함된 모델들과 동일한 모델만 반환합니다.

```
use App\Models\User;

$users = $users->intersect(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-load"></a>
<!-- #### `load($relations)` -->
#### `load($relations)`

<!-- The `load` method eager loads the given relationships for all models in the collection: -->
`load` 메서드는 컬렉션 내 모든 모델에 대해 지정한 연관관계를 즉시 로드(eager load)합니다.

```
$users->load(['comments', 'posts']);

$users->load('comments.author');

$users->load(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-loadMissing"></a>
<!-- #### `loadMissing($relations)` -->
#### `loadMissing($relations)`

<!-- The `loadMissing` method eager loads the given relationships for all models in the collection if the relationships are not already loaded: -->
`loadMissing` 메서드는 컬렉션 내 모든 모델에 대해 아직 불러오지 않은 연관관계만 즉시 로드(eager load)합니다.

```
$users->loadMissing(['comments', 'posts']);

$users->loadMissing('comments.author');

$users->loadMissing(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-modelKeys"></a>
<!-- #### `modelKeys()` -->
#### `modelKeys()`

<!-- The `modelKeys` method returns the primary keys for all models in the collection: -->
`modelKeys` 메서드는 컬렉션에 포함된 모든 모델의 기본키(primary key)를 반환합니다.

```
$users->modelKeys();

// [1, 2, 3, 4, 5]
```

<a name="method-makeVisible"></a>
<!-- #### `makeVisible($attributes)` -->
#### `makeVisible($attributes)`

<!-- The `makeVisible` method [makes attributes visible](/docs/11.x/eloquent-serialization#hiding-attributes-from-json) that are typically "hidden" on each model in the collection: -->
`makeVisible` 메서드는 기본적으로 "숨김(hidden)" 처리된 속성들을 [makes attributes visible](/docs/11.x/eloquent-serialization#hiding-attributes-from-json)합니다.

```
$users = $users->makeVisible(['address', 'phone_number']);
```

<a name="method-makeHidden"></a>
<!-- #### `makeHidden($attributes)` -->
#### `makeHidden($attributes)`

<!-- The `makeHidden` method [hides attributes](/docs/11.x/eloquent-serialization#hiding-attributes-from-json) that are typically "visible" on each model in the collection: -->
`makeHidden` 메서드는 기본적으로 "보임(visible)" 처리된 속성들을 [hides attributes](/docs/11.x/eloquent-serialization#hiding-attributes-from-json)합니다.

```
$users = $users->makeHidden(['address', 'phone_number']);
```

<a name="method-only"></a>
<!-- #### `only($keys)` -->
#### `only($keys)`

<!-- The `only` method returns all of the models that have the given primary keys: -->
`only` 메서드는 인자로 전달한 기본키(primary key)와 일치하는 모델만 반환합니다.

```
$users = $users->only([1, 2, 3]);
```

<a name="method-setVisible"></a>
<!-- #### `setVisible($attributes)` -->
#### `setVisible($attributes)`

<!-- The `setVisible` method [temporarily overrides](/docs/11.x/eloquent-serialization#temporarily-modifying-attribute-visibility) all of the visible attributes on each model in the collection: -->
`setVisible` 메서드는 컬렉션 내 모든 모델의 보이는 속성(visible attributes)을 [temporarily overrides](/docs/11.x/eloquent-serialization#temporarily-modifying-attribute-visibility).

```
$users = $users->setVisible(['id', 'name']);
```

<a name="method-setHidden"></a>
<!-- #### `setHidden($attributes)` -->
#### `setHidden($attributes)`

<!-- The `setHidden` method [temporarily overrides](/docs/11.x/eloquent-serialization#temporarily-modifying-attribute-visibility) all of the hidden attributes on each model in the collection: -->
`setHidden` 메서드는 컬렉션 내 모든 모델의 숨긴 속성(hidden attributes)을 [temporarily overrides](/docs/11.x/eloquent-serialization#temporarily-modifying-attribute-visibility).

```
$users = $users->setHidden(['email', 'password', 'remember_token']);
```

<a name="method-toquery"></a>
<!-- #### `toQuery()` -->
#### `toQuery()`

<!-- The `toQuery` method returns an Eloquent query builder instance containing a `whereIn` constraint on the collection model's primary keys: -->
`toQuery` 메서드는 컬렉션에 포함된 모델들의 기본키(primary key)를 대상으로 `whereIn` 조건이 적용된 Eloquent 쿼리 빌더 인스턴스를 반환합니다.

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

<!-- The `unique` method returns all of the unique models in the collection. Any models with the same primary key as another model in the collection are removed: -->
`unique` 메서드는 컬렉션 내에서 기본키(primary key)가 중복되지 않는 유일한 모델만을 반환합니다. 즉, 중복된 기본키를 가진 모델은 모두 제거됩니다.

```
$users = $users->unique();
```

<a name="custom-collections"></a>
<!-- ## Custom Collections -->
## Custom Collections

<!-- If you would like to use a custom `Collection` object when interacting with a given model, you may add the `CollectedBy` attribute to your model: -->
특정 모델을 다룰 때 기본 `Collection` 객체 대신 직접 정의한 커스텀 컬렉션 객체를 사용하고 싶다면, 해당 모델에 `CollectedBy` 특성(attribute)을 추가하면 됩니다.

```
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
또는, 모델 클래스에 `newCollection` 메서드를 직접 정의하여 사용할 수도 있습니다.

```
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
        return new UserCollection($models);
    }
}
```

<!-- Once you have defined a `newCollection` method or added the `CollectedBy` attribute to your model, you will receive an instance of your custom collection anytime Eloquent would normally return an `Illuminate\Database\Eloquent\Collection` instance. -->
`newCollection` 메서드를 정의하거나, `CollectedBy` 특성을 모델에 추가하면, Eloquent가 원래 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하던 모든 상황에서 여러분이 정의한 커스텀 컬렉션 인스턴스를 대신 반환하게 됩니다.

<!-- If you would like to use a custom collection for every model in your application, you should define the `newCollection` method on a base model class that is extended by all of your application's models. -->
또 하나 팁을 더하자면, 애플리케이션 내 모든 모델에 대해 동일한 커스텀 컬렉션을 사용하고 싶다면, 공통으로 상속받는 베이스 모델 클래스에 `newCollection` 메서드를 정의하면 됩니다.
