# Eloquent: 컬렉션 (Eloquent: Collections)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [커스텀 컬렉션](#custom-collections)

<a name="introduction"></a>
## 소개 (Introduction)

둘 이상의 모델 결과를 반환하는 모든 Eloquent 메서드는 `get` 메서드를 통해 검색되거나 관계를 통해 액세스되는 결과를 포함하여 `Illuminate\Database\Eloquent\Collection` 클래스의 인스턴스를 반환합니다. Eloquent 컬렉션 개체는 Laravel의 [기본 컬렉션](/docs/13.x/collections)을 확장하므로 Eloquent 모델의 기본 배열을 원활하게 작업하는 데 사용되는 수십 가지 메서드를 자연스럽게 상속합니다. 이러한 유용한 메서드에 대해 자세히 알아보려면 Laravel 컬렉션 문서를 참고하세요!

모든 컬렉션은 반복자 역할도 하므로 단순한 PHP 배열인 것처럼 반복할 수 있습니다.

```php
use App\Models\User;

$users = User::where('active', 1)->get();

foreach ($users as $user) {
    echo $user->name;
}
```

그러나 앞서 언급했듯이 컬렉션은 배열보다 훨씬 강력하며 직관적인 인터페이스를 사용하여 연결될 수 있는 다양한 맵/리듀스 작업을 제공합니다. 예를 들어, 모든 비활성 모델을 제거한 다음 나머지 각 사용자의 이름을 수집할 수 있습니다.

```php
$names = User::all()->reject(function (User $user) {
    return $user->active === false;
})->map(function (User $user) {
    return $user->name;
});
```

<a name="eloquent-collection-conversion"></a>
#### Eloquent 컬렉션 변환

대부분의 Eloquent 컬렉션 메서드는 Eloquent 컬렉션의 새 인스턴스를 반환하지만, `collapse`, `flatten`, `flip`, `keys`, `pluck` 및 `zip` 메서드는 [기본 컬렉션](/docs/13.x/collections) 인스턴스를 반환합니다. 마찬가지로, `map` 작업이 Eloquent 모델을 포함하지 않는 컬렉션을 반환하는 경우 기본 컬렉션 인스턴스로 변환됩니다.

<a name="available-methods"></a>
## 사용 가능한 메서드 (Available Methods)

모든 Eloquent 컬렉션은 기본 [Laravel 컬렉션](/docs/13.x/collections#available-methods) 개체를 확장합니다. 따라서 기본 컬렉션 클래스에서 제공하는 강력한 메서드를 모두 상속합니다.

또한 `Illuminate\Database\Eloquent\Collection` 클래스는 모델 컬렉션 관리에 도움이 되는 메서드의 상위 집합을 제공합니다. 대부분의 메서드는 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환합니다. 그러나 `modelKeys`와 같은 일부 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환합니다.

<style>{`
    .collection-method-list > p {
        columns: 14.4em 1; -moz-columns: 14.4em 1; -webkit-columns: 14.4em 1;
    }

    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .collection-method code {
        font-size: 14px;
    }

    .collection-method:not(.first-collection-method) {
        margin-top: 50px;
    }
`}</style>

<div class="collection-method-list" markdown="1">

[추가](#method-append)
[포함](#method-contains)
[차이](#method-diff)
[제외](#method-except)
[찾기](#method-find)
[찾기 또는 실패](#method-find-or-fail)
[신선한](#method-fresh)
[교차](#method-intersect)
[로드](#method-load)
[로드 누락](#method-loadMissing)
[모델키](#method-modelKeys)
[makeVisible](#method-makeVisible)
[makeHidden](#method-makeHidden)
[병합 표시](#method-mergeVisible)
[병합숨김](#method-mergeHidden)
[만](#method-only)
[파티션](#method-partition)
[세트추가](#method-setAppends)
[설정표시](#method-setVisible)
[설정숨김](#method-setHidden)
[쿼리](#method-toquery)
[고유](#method-unique)
[추가 없음](#method-withoutAppends)

</div>

<a name="method-append"></a>
#### `append($attributes)`
`append` 메서드는 컬렉션의 모든 모델에 대해 속성이 [추가](/docs/13.x/eloquent-serialization#appending-values-to-json)되어야 함을 나타내는 데 사용될 수 있습니다. 이 메서드는 속성 배열 또는 단일 속성을 허용합니다.

```php
$users->append('team');

$users->append(['team', 'is_admin']);
```

<a name="method-contains"></a>
#### `contains($key, $operator = null, $value = null)`
`contains` 메서드는 주어진 모델 인스턴스가 컬렉션에 포함되어 있는지 확인하는 데 사용될 수 있습니다. 이 메서드는 기본 키 또는 모델 인스턴스를 허용합니다.

```php
$users->contains(1);

$users->contains(User::find(1));
```

<a name="method-diff"></a>
#### `diff($items)`
`diff` 메서드는 지정된 컬렉션에 없는 모든 모델을 반환합니다.

```php
use App\Models\User;

$users = $users->diff(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-except"></a>
#### `except($keys)`
`except` 메서드는 지정된 기본 키가 없는 모든 모델을 반환합니다.

```php
$users = $users->except([1, 2, 3]);
```

<a name="method-find"></a>
#### `find($key)`
`find` 메서드는 지정된 키와 일치하는 기본 키가 있는 모델을 반환합니다. `$key`가 모델 인스턴스인 경우 `find`는 기본 키와 일치하는 모델을 반환하려고 시도합니다. `$key`가 키 배열인 경우 `find`는 지정된 배열에 기본 키가 있는 모든 모델을 반환합니다.

```php
$users = User::all();

$user = $users->find(1);
```

<a name="method-find-or-fail"></a>
#### `findOrFail($key)`
`findOrFail` 메서드는 지정된 키와 일치하는 기본 키가 있는 모델을 반환하거나 컬렉션에서 일치하는 모델을 찾을 수 없는 경우 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 발생시킵니다.

```php
$users = User::all();

$user = $users->findOrFail(1);
```

<a name="method-fresh"></a>
#### `fresh($with = [])`
`fresh` 메서드는 데이터베이스에서 컬렉션에 있는 각 모델의 새 인스턴스를 검색합니다. 또한 지정된 관계가 모두 즉시 로드됩니다.

```php
$users = $users->fresh();

$users = $users->fresh('comments');
```

<a name="method-intersect"></a>
#### `intersect($items)`
`intersect` 메서드는 지정된 컬렉션에도 존재하는 모든 모델을 반환합니다.

```php
use App\Models\User;

$users = $users->intersect(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-load"></a>
#### `load($relations)`
`load` 메서드는 컬렉션의 모든 모델에 대해 지정된 관계를 로드합니다.

```php
$users->load(['comments', 'posts']);

$users->load('comments.author');

$users->load(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-loadMissing"></a>
#### `loadMissing($relations)`
`loadMissing` 메서드는 관계가 아직 로드되지 않은 경우 컬렉션의 모든 모델에 대해 지정된 관계를 로드합니다.

```php
$users->loadMissing(['comments', 'posts']);

$users->loadMissing('comments.author');

$users->loadMissing(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-modelKeys"></a>
#### `modelKeys()`
`modelKeys` 메서드는 컬렉션의 모든 모델에 대한 기본 키를 반환합니다.

```php
$users->modelKeys();

// [1, 2, 3, 4, 5]
```

<a name="method-makeVisible"></a>
#### `makeVisible($attributes)`
`makeVisible` 메서드는 일반적으로 컬렉션의 각 모델에 "숨겨진" [속성을 표시](/docs/13.x/eloquent-serialization#hiding-attributes-from-json)합니다.

```php
$users = $users->makeVisible(['address', 'phone_number']);
```

<a name="method-makeHidden"></a>
#### `makeHidden($attributes)`
`makeHidden` 메서드는 컬렉션의 각 모델에서 일반적으로 "표시"되는 [속성을 숨깁니다](/docs/13.x/eloquent-serialization#hiding-attributes-from-json):

```php
$users = $users->makeHidden(['address', 'phone_number']);
```

<a name="method-mergeVisible"></a>
#### `mergeVisible($attributes)`
`mergeVisible` 메서드는 기존 가시 속성을 유지하면서 [추가 속성을 표시](/docs/13.x/eloquent-serialization#hiding-attributes-from-json)합니다.

```php
$users = $users->mergeVisible(['middle_name']);
```

<a name="method-mergeHidden"></a>
#### `mergeHidden($attributes)`
`mergeHidden` 방법은 기존 숨겨진 속성을 유지하면서 [추가 속성을 숨깁니다](/docs/13.x/eloquent-serialization#hiding-attributes-from-json):

```php
$users = $users->mergeHidden(['last_login_at']);
```

<a name="method-only"></a>
#### `only($keys)`
`only` 메서드는 지정된 기본 키가 있는 모든 모델을 반환합니다.

```php
$users = $users->only([1, 2, 3]);
```

<a name="method-partition"></a>
#### `partition`
`partition` 메서드는 `Illuminate\Database\Eloquent\Collection` 컬렉션 인스턴스를 포함하는 `Illuminate\Support\Collection` 인스턴스를 반환합니다.

```php
$partition = $users->partition(fn ($user) => $user->age > 18);

dump($partition::class);    // Illuminate\Support\Collection
dump($partition[0]::class); // Illuminate\Database\Eloquent\Collection
dump($partition[1]::class); // Illuminate\Database\Eloquent\Collection
```

<a name="method-setAppends"></a>
#### `setAppends($attributes)`
`setAppends` 메서드는 컬렉션의 각 모델에 대한 모든 [추가된 속성](/docs/13.x/eloquent-serialization#appending-values-to-json)을 일시적으로 재정의합니다.

```php
$users = $users->setAppends(['is_admin']);
```

<a name="method-setVisible"></a>
#### `setVisible($attributes)`
`setVisible` 메서드는 컬렉션의 각 모델에 표시되는 모든 속성을 [일시적으로 재정의](/docs/13.x/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다.

```php
$users = $users->setVisible(['id', 'name']);
```

<a name="method-setHidden"></a>
#### `setHidden($attributes)`
`setHidden` 메서드는 컬렉션의 각 모델에 대한 모든 숨겨진 속성을 [일시적으로 재정의](/docs/13.x/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다.

```php
$users = $users->setHidden(['email', 'password', 'remember_token']);
```

<a name="method-toquery"></a>
#### `toQuery()`
`toQuery` 메서드는 컬렉션 모델의 기본 키에 대한 `whereIn` 제약 조건을 포함하는 Eloquent 쿼리 빌더 인스턴스를 반환합니다.

```php
use App\Models\User;

$users = User::where('status', 'VIP')->get();

$users->toQuery()->update([
    'status' => 'Administrator',
]);
```

<a name="method-unique"></a>
#### `unique($key = null, $strict = false)`
`unique` 메서드는 컬렉션의 고유한 모델을 모두 반환합니다. 컬렉션의 다른 모델와 동일한 기본 키를 가진 모든 모델이 제거됩니다.

```php
$users = $users->unique();
```

<a name="method-withoutAppends"></a>
#### `withoutAppends()`
`withoutAppends` 메서드는 컬렉션의 각 모델에서 모든 [추가된 속성](/docs/13.x/eloquent-serialization#appending-values-to-json)을 일시적으로 제거합니다.

```php
$users = $users->withoutAppends();
```

<a name="custom-collections"></a>
## 커스텀 컬렉션 (Custom Collections)

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

`newCollection` 메서드를 정의하거나 모델에 `CollectedBy` 속성을 추가하면 Eloquent가 일반적으로 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환할 때마다 사용자 지정 컬렉션의 인스턴스를 받게 됩니다.

애플리케이션의 모든 모델에 대해 사용자 지정 컬렉션을 사용하려면 애플리케이션의 모든 모델에 의해 확장되는 기본 모델 클래스에 `newCollection` 메서드를 정의해야 합니다.
