# 일러퀀트: 컬렉션 (Eloquent: Collections)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [커스텀 컬렉션](#custom-collections)

<a name="introduction"></a>
## 소개 (Introduction)

하나 이상의 모델 결과를 반환하는 모든 Eloquent 메서드는 `Illuminate\Database\Eloquent\Collection` 클래스의 인스턴스를 반환합니다. 이는 `get` 메서드를 사용하여 조회하거나, 연관관계를 통해 접근할 때도 마찬가지입니다. Eloquent 컬렉션 객체는 Laravel의 [기본 컬렉션](/docs/12.x/collections)을 확장하므로, Eloquent 모델 배열을 유연하게 다루기 위한 다양한 메서드를 자연스럽게 상속합니다. 실무에 유용한 이 메서드들을 모두 익히기 위해, Laravel 컬렉션 문서를 꼭 참고하시기 바랍니다!

모든 컬렉션은 반복자(iterator)로도 동작하므로, 마치 일반 PHP 배열처럼 반복문으로 순회할 수 있습니다:

```php
use App\Models\User;

$users = User::where('active', 1)->get();

foreach ($users as $user) {
    echo $user->name;
}
```

하지만 앞서 언급했듯이, 컬렉션은 단순한 배열보다 훨씬 강력하며, 직관적인 인터페이스를 통해 메서드를 연결하여 다양한 map/reduce 연산을 수행할 수 있습니다. 예를 들어, 비활성화된 모델을 제거한 후 남아있는 각 사용자의 이름만 추출할 수 있습니다:

```php
$names = User::all()->reject(function (User $user) {
    return $user->active === false;
})->map(function (User $user) {
    return $user->name;
});
```

<a name="eloquent-collection-conversion"></a>
#### 일러퀀트 컬렉션 변환

대부분의 Eloquent 컬렉션 메서드는 새로운 Eloquent 컬렉션 인스턴스를 반환합니다. 그러나 `collapse`, `flatten`, `flip`, `keys`, `pluck`, `zip` 메서드는 [기본 컬렉션](/docs/12.x/collections) 인스턴스를 반환합니다. 또한, `map` 연산의 결과에 Eloquent 모델이 하나도 포함되어 있지 않으면, 해당 컬렉션은 자동으로 기본 컬렉션 인스턴스로 변환됩니다.

<a name="available-methods"></a>
## 사용 가능한 메서드 (Available Methods)

모든 Eloquent 컬렉션은 [Laravel 기본 컬렉션](/docs/12.x/collections#available-methods) 객체를 확장하므로, 기본 컬렉션 클래스에서 제공하는 강력한 메서드들을 모두 사용할 수 있습니다.

더불어, `Illuminate\Database\Eloquent\Collection` 클래스는 모델 컬렉션을 관리하는 데 도움이 되는 다양한 고유 메서드도 제공합니다. 대부분의 메서드는 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하지만, `modelKeys`와 같은 일부 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환합니다.

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

`append` 메서드는 컬렉션 내 모든 모델에 [속성 추가](/docs/12.x/eloquent-serialization#appending-values-to-json)가 필요할 때 사용합니다. 배열이나 단일 속성을 인수로 받을 수 있습니다.

```php
$users->append('team');

$users->append(['team', 'is_admin']);
```

<a name="method-contains"></a>
#### `contains($key, $operator = null, $value = null)`

`contains` 메서드는 컬렉션에 특정 모델 인스턴스 또는 기본 키(primary key)가 포함되어 있는지 확인합니다.

```php
$users->contains(1);

$users->contains(User::find(1));
```

<a name="method-diff"></a>
#### `diff($items)`

`diff` 메서드는 주어진 컬렉션에 없는 모든 모델을 반환합니다.

```php
use App\Models\User;

$users = $users->diff(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-except"></a>
#### `except($keys)`

`except` 메서드는 제공한 기본 키에 해당하지 않는 모든 모델을 반환합니다.

```php
$users = $users->except([1, 2, 3]);
```

<a name="method-find"></a>
#### `find($key)`

`find` 메서드는 주어진 키와 일치하는 기본 키(primary key)를 가진 모델을 반환합니다. `$key`가 모델 인스턴스라면, 해당 원본과 동일한 기본 키의 모델을 반환하려고 시도합니다. `$key`에 배열을 전달하면, 해당 배열 내의 기본 키를 가진 모든 모델을 반환합니다.

```php
$users = User::all();

$user = $users->find(1);
```

<a name="method-find-or-fail"></a>
#### `findOrFail($key)`

`findOrFail` 메서드는 주어진 키와 일치하는 기본 키를 가진 모델을 반환하거나, 컬렉션 안에 찾는 모델이 없을 경우 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 발생시킵니다.

```php
$users = User::all();

$user = $users->findOrFail(1);
```

<a name="method-fresh"></a>
#### `fresh($with = [])`

`fresh` 메서드는 컬렉션의 모든 모델에 대해 데이터베이스에서 새 인스턴스를 조회합니다. 또한, 지정한 연관관계도 eager loading 할 수 있습니다.

```php
$users = $users->fresh();

$users = $users->fresh('comments');
```

<a name="method-intersect"></a>
#### `intersect($items)`

`intersect` 메서드는 주어진 컬렉션에 이미 존재하는 모델만 반환합니다.

```php
use App\Models\User;

$users = $users->intersect(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-load"></a>
#### `load($relations)`

`load` 메서드는 컬렉션 내 모든 모델에 대해 지정한 연관관계를 eager loading(즉시 로딩)합니다.

```php
$users->load(['comments', 'posts']);

$users->load('comments.author');

$users->load(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-loadMissing"></a>
#### `loadMissing($relations)`

`loadMissing` 메서드는 지정한 연관관계가 이미 로딩되어 있지 않은 경우에만 컬렉션 내 모든 모델에 대해 eager loading합니다.

```php
$users->loadMissing(['comments', 'posts']);

$users->loadMissing('comments.author');

$users->loadMissing(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-modelKeys"></a>
#### `modelKeys()`

`modelKeys` 메서드는 컬렉션 내 모든 모델의 기본 키 배열을 반환합니다.

```php
$users->modelKeys();

// [1, 2, 3, 4, 5]
```

<a name="method-makeVisible"></a>
#### `makeVisible($attributes)`

`makeVisible` 메서드는 컬렉션 내 모든 모델의 [숨겨진(hidden) 속성](/docs/12.x/eloquent-serialization#hiding-attributes-from-json)을 표시하도록 만듭니다.

```php
$users = $users->makeVisible(['address', 'phone_number']);
```

<a name="method-makeHidden"></a>
#### `makeHidden($attributes)`

`makeHidden` 메서드는 컬렉션 내 모든 모델의 [노출(visible) 속성](/docs/12.x/eloquent-serialization#hiding-attributes-from-json)을 숨기도록 만듭니다.

```php
$users = $users->makeHidden(['address', 'phone_number']);
```

<a name="method-mergeVisible"></a>
#### `mergeVisible($attributes)`

`mergeVisible` 메서드는 기존 노출 속성은 그대로 두고, [추가 속성을 노출](/docs/12.x/eloquent-serialization#hiding-attributes-from-json)시킵니다.

```php
$users = $users->mergeVisible(['middle_name']);
```

<a name="method-mergeHidden"></a>
#### `mergeHidden($attributes)`

`mergeHidden` 메서드는 기존 숨겨진 속성은 유지하면서, [추가 속성을 숨김](/docs/12.x/eloquent-serialization#hiding-attributes-from-json) 처리할 수 있습니다.

```php
$users = $users->mergeHidden(['last_login_at']);
```

<a name="method-only"></a>
#### `only($keys)`

`only` 메서드는 전달한 기본 키를 가진 모든 모델만 반환합니다.

```php
$users = $users->only([1, 2, 3]);
```

<a name="method-partition"></a>
#### `partition`

`partition` 메서드는 두 개의 `Illuminate\Database\Eloquent\Collection` 인스턴스가 포함된 `Illuminate\Support\Collection` 인스턴스를 반환합니다.

```php
$partition = $users->partition(fn ($user) => $user->age > 18);

dump($partition::class);    // Illuminate\Support\Collection
dump($partition[0]::class); // Illuminate\Database\Eloquent\Collection
dump($partition[1]::class); // Illuminate\Database\Eloquent\Collection
```

<a name="method-setAppends"></a>
#### `setAppends($attributes)`

`setAppends` 메서드는 컬렉션 내 모든 모델의 [추가 속성(appended attributes)](/docs/12.x/eloquent-serialization#appending-values-to-json)을 임시로 덮어씁니다.

```php
$users = $users->setAppends(['is_admin']);
```

<a name="method-setVisible"></a>
#### `setVisible($attributes)`

`setVisible` 메서드는 컬렉션 내 모든 모델의 노출 속성을 [임시로 덮어쓰기](/docs/12.x/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다.

```php
$users = $users->setVisible(['id', 'name']);
```

<a name="method-setHidden"></a>
#### `setHidden($attributes)`

`setHidden` 메서드는 컬렉션 내 모든 모델에서 숨길 속성을 [임시로 덮어쓰기](/docs/12.x/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다.

```php
$users = $users->setHidden(['email', 'password', 'remember_token']);
```

<a name="method-toquery"></a>
#### `toQuery()`

`toQuery` 메서드는 컬렉션의 모델 기본 키를 대상으로 하는 `whereIn` 조건이 적용된 Eloquent 쿼리 빌더 인스턴스를 반환합니다.

```php
use App\Models\User;

$users = User::where('status', 'VIP')->get();

$users->toQuery()->update([
    'status' => 'Administrator',
]);
```

<a name="method-unique"></a>
#### `unique($key = null, $strict = false)`

`unique` 메서드는 컬렉션 내에서 중복된 기본 키를 가진 모델을 제거하고, 유일한 모델만 반환합니다.

```php
$users = $users->unique();
```

<a name="method-withoutAppends"></a>
#### `withoutAppends()`

`withoutAppends` 메서드는 컬렉션 내 모든 모델의 [추가 속성(appended attributes)](/docs/12.x/eloquent-serialization#appending-values-to-json)을 임시로 제거합니다.

```php
$users = $users->withoutAppends();
```

<a name="custom-collections"></a>
## 커스텀 컬렉션 (Custom Collections)

특정 모델을 사용할 때 커스텀 `Collection` 객체를 이용하고 싶다면, 모델에 `CollectedBy` 속성(attribute)을 추가할 수 있습니다:

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

또는, 모델에 `newCollection` 메서드를 정의하는 방법도 있습니다:

```php
<?php

namespace App\Models;

use App\Support\UserCollection;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 새로운 Eloquent 컬렉션 인스턴스를 생성합니다.
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

`newCollection` 메서드를 정의하거나 모델에 `CollectedBy` 속성을 추가하면, Eloquent가 일반적으로 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하는 위치에서 항상 커스텀 컬렉션 인스턴스를 반환하게 됩니다.

애플리케이션의 모든 모델에 대해 커스텀 컬렉션을 사용하고 싶다면, 공통이 되는 베이스 모델 클래스에 `newCollection` 메서드를 정의하고, 이 베이스 클래스를 각 모델들이 상속받도록 구성하면 됩니다.