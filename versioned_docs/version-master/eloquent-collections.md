# Eloquent: 컬렉션 (Eloquent: Collections)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [커스텀 컬렉션](#custom-collections)

<a name="introduction"></a>
## 소개

여러 개의 모델 결과를 반환하는 모든 Eloquent 메서드는 `Illuminate\Database\Eloquent\Collection` 클래스의 인스턴스를 반환합니다. 이는 `get` 메서드로 검색된 결과나 연관관계(relationship)를 통해 접근하는 경우도 포함됩니다. Eloquent 컬렉션 객체는 Laravel의 [기본 컬렉션](/docs/master/collections)을 확장하므로, Eloquent 모델 배열을 유연하게 다룰 수 있도록 수십 가지의 메서드를 자연스럽게 상속받습니다. 유용한 메서드에 대해 더 알고 싶다면 Laravel 컬렉션 문서를 꼭 참고하시기 바랍니다!

컬렉션은 반복자(iterator) 역할도 하므로, 일반 PHP 배열처럼 반복문을 사용할 수 있습니다:

```php
use App\Models\User;

$users = User::where('active', 1)->get();

foreach ($users as $user) {
    echo $user->name;
}
```

하지만 앞서 설명했듯이, 컬렉션은 배열보다 훨씬 강력하여 다양한 map/reduce 연산을 직관적인 방식으로 연결(chain)할 수 있습니다. 예를 들어, 비활성화된 모델을 모두 제거한 뒤 남은 사용자들의 이름만 모을 수도 있습니다:

```php
$names = User::all()->reject(function (User $user) {
    return $user->active === false;
})->map(function (User $user) {
    return $user->name;
});
```

<a name="eloquent-collection-conversion"></a>
#### Eloquent 컬렉션 변환

대부분의 Eloquent 컬렉션 메서드는 새로운 Eloquent 컬렉션 인스턴스를 반환합니다. 하지만 `collapse`, `flatten`, `flip`, `keys`, `pluck`, `zip` 메서드는 [기본 컬렉션](/docs/master/collections) 인스턴스를 반환합니다. 또한, `map` 연산의 결과가 Eloquent 모델을 포함하지 않으면, 해당 결과는 자동으로 기본 컬렉션 인스턴스로 변환됩니다.

<a name="available-methods"></a>
## 사용 가능한 메서드

모든 Eloquent 컬렉션은 기본 [Laravel 컬렉션](/docs/master/collections#available-methods) 객체를 확장하므로, 기본 컬렉션 클래스가 제공하는 강력한 모든 메서드를 상속받습니다.

이와 더불어, `Illuminate\Database\Eloquent\Collection` 클래스는 모델 컬렉션을 다루는 데 도움이 되는 몇 가지 추가 메서드를 제공합니다. 대부분의 메서드는 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하지만, `modelKeys`와 같이 일부 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환합니다.


<div class="collection-method-list" markdown="1">

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

</div>

<a name="method-append"></a>
#### `append($attributes)`

`append` 메서드는 컬렉션 내의 모든 모델에 대해 [속성 추가](/docs/master/eloquent-serialization#appending-values-to-json)가 필요할 때 사용합니다. 이 메서드는 속성 배열이나 단일 속성을 인수로 받을 수 있습니다:

```php
$users->append('team');

$users->append(['team', 'is_admin']);
```

<a name="method-contains"></a>
#### `contains($key, $operator = null, $value = null)`

`contains` 메서드는 주어진 모델 인스턴스가 컬렉션에 포함되어 있는지 확인할 때 사용합니다. 인수로 기본 키 또는 모델 인스턴스를 전달할 수 있습니다:

```php
$users->contains(1);

$users->contains(User::find(1));
```

<a name="method-diff"></a>
#### `diff($items)`

`diff` 메서드는 전달한 컬렉션에 존재하지 않는 모델만 반환합니다:

```php
use App\Models\User;

$users = $users->diff(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-except"></a>
#### `except($keys)`

`except` 메서드는 지정한 기본 키를 가진 모델을 제외한 모든 모델을 반환합니다:

```php
$users = $users->except([1, 2, 3]);
```

<a name="method-find"></a>
#### `find($key)`

`find` 메서드는 전달한 키와 일치하는 기본 키를 가진 모델을 반환합니다. `$key`가 모델 인스턴스라면, 해당 기본 키로 모델을 반환합니다. 배열 형태로 키를 넘기면, 일치하는 모든 모델을 반환합니다:

```php
$users = User::all();

$user = $users->find(1);
```

<a name="method-find-or-fail"></a>
#### `findOrFail($key)`

`findOrFail` 메서드는 주어진 기본 키와 일치하는 모델을 반환하거나, 찾지 못할 경우 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 발생시킵니다:

```php
$users = User::all();

$user = $users->findOrFail(1);
```

<a name="method-fresh"></a>
#### `fresh($with = [])`

`fresh` 메서드는 컬렉션 내의 각 모델에 대해 데이터베이스에서 새로운 인스턴스를 가져옵니다. 이때 지정한 연관관계가 있으면 eager loading도 수행합니다:

```php
$users = $users->fresh();

$users = $users->fresh('comments');
```

<a name="method-intersect"></a>
#### `intersect($items)`

`intersect` 메서드는 전달한 컬렉션에도 포함되어 있는 모델만 반환합니다:

```php
use App\Models\User;

$users = $users->intersect(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-load"></a>
#### `load($relations)`

`load` 메서드는 컬렉션 내 모든 모델에 대해 지정한 연관관계를 eager loading합니다:

```php
$users->load(['comments', 'posts']);

$users->load('comments.author');

$users->load(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-loadMissing"></a>
#### `loadMissing($relations)`

`loadMissing` 메서드는 아직 로드되지 않은 지정한 연관관계만 eager loading합니다:

```php
$users->loadMissing(['comments', 'posts']);

$users->loadMissing('comments.author');

$users->loadMissing(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-modelKeys"></a>
#### `modelKeys()`

`modelKeys` 메서드는 컬렉션 내 모든 모델의 기본 키를 반환합니다:

```php
$users->modelKeys();

// [1, 2, 3, 4, 5]
```

<a name="method-makeVisible"></a>
#### `makeVisible($attributes)`

`makeVisible` 메서드는 컬렉션 내 각 모델에서 주로 "숨김(hidden)" 처리된 속성을 [표시](/docs/master/eloquent-serialization#hiding-attributes-from-json)하도록 만듭니다:

```php
$users = $users->makeVisible(['address', 'phone_number']);
```

<a name="method-makeHidden"></a>
#### `makeHidden($attributes)`

`makeHidden` 메서드는 컬렉션 내 각 모델에서 주로 "노출(visible)"되어 있던 속성을 [감추기](/docs/master/eloquent-serialization#hiding-attributes-from-json) 처리합니다:

```php
$users = $users->makeHidden(['address', 'phone_number']);
```

<a name="method-mergeVisible"></a>
#### `mergeVisible($attributes)`

`mergeVisible` 메서드는 기존의 노출(visible) 속성을 유지하면서 [추가로 노출할 속성](/docs/master/eloquent-serialization#hiding-attributes-from-json)을 지정할 때 사용합니다:

```php
$users = $users->mergeVisible(['middle_name']);
```

<a name="method-mergeHidden"></a>
#### `mergeHidden($attributes)`

`mergeHidden` 메서드는 기존의 숨김(hidden) 속성을 유지하면서 [추가로 숨길 속성](/docs/master/eloquent-serialization#hiding-attributes-from-json)을 지정할 때 사용합니다:

```php
$users = $users->mergeHidden(['last_login_at']);
```

<a name="method-only"></a>
#### `only($keys)`

`only` 메서드는 지정한 기본 키를 가진 모든 모델을 반환합니다:

```php
$users = $users->only([1, 2, 3]);
```

<a name="method-partition"></a>
#### `partition`

`partition` 메서드는 조건에 따라 컬렉션을 분할한 결과를 담은 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 각 파티션은 `Illuminate\Database\Eloquent\Collection` 인스턴스입니다:

```php
$partition = $users->partition(fn ($user) => $user->age > 18);

dump($partition::class);    // Illuminate\Support\Collection
dump($partition[0]::class); // Illuminate\Database\Eloquent\Collection
dump($partition[1]::class); // Illuminate\Database\Eloquent\Collection
```

<a name="method-setAppends"></a>
#### `setAppends($attributes)`

`setAppends` 메서드는 컬렉션 내 각 모델의 [appended 속성](/docs/master/eloquent-serialization#appending-values-to-json)을 임시로 덮어씁니다:

```php
$users = $users->setAppends(['is_admin']);
```

<a name="method-setVisible"></a>
#### `setVisible($attributes)`

`setVisible` 메서드는 컬렉션 내 각 모델의 노출(visible) 속성을 [임시로 재정의](/docs/master/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다:

```php
$users = $users->setVisible(['id', 'name']);
```

<a name="method-setHidden"></a>
#### `setHidden($attributes)`

`setHidden` 메서드는 컬렉션 내 각 모델의 숨김(hidden) 속성을 [임시로 재정의](/docs/master/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다:

```php
$users = $users->setHidden(['email', 'password', 'remember_token']);
```

<a name="method-toquery"></a>
#### `toQuery()`

`toQuery` 메서드는 컬렉션의 모델 기본 키에 대해 `whereIn` 조건이 적용된 Eloquent 쿼리 빌더 인스턴스를 반환합니다:

```php
use App\Models\User;

$users = User::where('status', 'VIP')->get();

$users->toQuery()->update([
    'status' => 'Administrator',
]);
```

<a name="method-unique"></a>
#### `unique($key = null, $strict = false)`

`unique` 메서드는 컬렉션 내에서 유일한 모든 모델을 반환합니다. 동일한 기본 키를 가진 중복 모델은 제거됩니다:

```php
$users = $users->unique();
```

<a name="method-withoutAppends"></a>
#### `withoutAppends()`

`withoutAppends` 메서드는 컬렉션 내 각 모델의 [appended 속성](/docs/master/eloquent-serialization#appending-values-to-json)을 임시로 모두 제거합니다:

```php
$users = $users->withoutAppends();
```

<a name="custom-collections"></a>
## 커스텀 컬렉션

특정 모델에서 커스텀 `Collection` 객체를 사용하고 싶다면, 모델에 `CollectedBy` 속성을 추가할 수 있습니다:

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

또는, 모델에서 `newCollection` 메서드를 정의할 수도 있습니다:

```php
<?php

namespace App\Models;

use App\Support\UserCollection;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 새로운 Eloquent Collection 인스턴스 생성.
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

`newCollection` 메서드를 정의하거나 모델에 `CollectedBy` 속성을 추가하면, Eloquent가 원래 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환할 상황에서도 커스텀 컬렉션 인스턴스를 받을 수 있습니다.

애플리케이션 내 모든 모델에 대해 커스텀 컬렉션을 사용하려면, 모든 모델이 상속받는 베이스 모델 클래스에 `newCollection` 메서드를 정의하세요.
