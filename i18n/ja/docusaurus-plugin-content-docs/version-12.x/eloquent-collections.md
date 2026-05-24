# Eloquent: コレクション (Eloquent: Collections)

- [Introduction](#introduction)
- [利用可能な方法](#available-methods)
- [カスタムコレクション](#custom-collections)

<a name="introduction"></a>
## 導入 (Introduction)

複数のモデル結果を返すすべての Eloquent メソッドは、`get` メソッドを介して取得された結果やリレーションシップを介してアクセスされた結果を含む、`Illuminate\Database\Eloquent\Collection` クラスのインスタンスを返します。 Eloquent コレクション オブジェクトは Laravel の [ベースコレクション](/docs/{{version}}/collections) を拡張するため、基礎となる Eloquent モデルの配列をスムーズに操作するために使用される多数のメソッドを自然に継承します。これらの便利なメソッドについて詳しく知るには、必ず Laravel コレクションのドキュメントを参照してください。

すべてのコレクションはイテレータとしても機能するため、単純な PHP 配列であるかのようにループすることができます。

```php
use App\Models\User;

$users = User::where('active', 1)->get();

foreach ($users as $user) {
    echo $user->name;
}
```

ただし、前述したように、コレクションは配列よりもはるかに強力で、直感的なインターフェイスを使用して連鎖できるさまざまなマップ/リデュース操作を公開します。たとえば、非アクティブなモデルをすべて削除し、残りの各ユーザーの名を収集します。

```php
$names = User::all()->reject(function (User $user) {
    return $user->active === false;
})->map(function (User $user) {
    return $user->name;
});
```

<a name="eloquent-collection-conversion"></a>
#### Eloquent コレクションの変換

ほとんどの Eloquent コレクション メソッドは Eloquent コレクションの新しいインスタンスを返しますが、`collapse`、`flatten`、`flip`、`keys`、`pluck`、および `zip` メソッドは [ベースコレクション](/docs/{{version}}/collections) インスタンスを返します。同様に、`map` オペレーションが Eloquent モデルを含まないコレクションを返す場合、それはベース コレクション インスタンスに変換されます。

<a name="available-methods"></a>
## 利用可能な方法 (Available Methods)

すべての Eloquent コレクションは、基本 [Laravelコレクション](/docs/{{version}}/collections#available-methods) オブジェクトを拡張します。したがって、これらは、基本コレクション クラスによって提供される強力なメソッドをすべて継承します。

さらに、`Illuminate\Database\Eloquent\Collection` クラスは、モデル コレクションの管理を支援するメソッドのスーパーセットを提供します。ほとんどのメソッドは `Illuminate\Database\Eloquent\Collection` インスタンスを返します。ただし、`modelKeys` などの一部のメソッドは、`Illuminate\Support\Collection` インスタンスを返します。

<style>
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
</style>

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
#### `append($attributes)` {.collection-method .first-collection-method}

`append` メソッドを使用して、コレクション内のすべてのモデルの属性が [appended](/docs/{{version}}/eloquent-serialization#appending-values-to-json) である必要があることを示すことができます。このメソッドは、属性の配列または単一の属性を受け入れます。

```php
$users->append('team');

$users->append(['team', 'is_admin']);
```

<a name="method-contains"></a>
#### `contains($key, $operator = null, $value = null)` {.collection-method}

`contains` メソッドは、特定のモデル インスタンスがコレクションに含まれているかどうかを判断するために使用できます。このメソッドは主キーまたはモデル インスタンスを受け入れます。

```php
$users->contains(1);

$users->contains(User::find(1));
```

<a name="method-diff"></a>
#### `diff($items)` {.collection-method}

`diff` メソッドは、指定されたコレクションに存在しないすべてのモデルを返します。

```php
use App\Models\User;

$users = $users->diff(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-except"></a>
#### `except($keys)` {.collection-method}

`except` メソッドは、指定された主キーを持たないすべてのモデルを返します。

```php
$users = $users->except([1, 2, 3]);
```

<a name="method-find"></a>
#### `find($key)` {.collection-method}

`find` メソッドは、指定されたキーに一致する主キーを持つモデルを返します。 `$key` がモデル インスタンスの場合、`find` は主キーに一致するモデルを返そうとします。 `$key` がキーの配列の場合、`find` は指定された配列に主キーを持つすべてのモデルを返します。

```php
$users = User::all();

$user = $users->find(1);
```

<a name="method-find-or-fail"></a>
#### `findOrFail($key)` {.collection-method}

`findOrFail` メソッドは、指定されたキーに一致する主キーを持つモデルを返すか、一致するモデルがコレクション内に見つからない場合は `Illuminate\Database\Eloquent\ModelNotFoundException` 例外をスローします。

```php
$users = User::all();

$user = $users->findOrFail(1);
```

<a name="method-fresh"></a>
#### `fresh($with = [])` {.collection-method}

`fresh` メソッドは、コレクション内の各モデルの新しいインスタンスをデータベースから取得します。さらに、指定された関係はすべて積極的にロードされます。

```php
$users = $users->fresh();

$users = $users->fresh('comments');
```

<a name="method-intersect"></a>
#### `intersect($items)` {.collection-method}

`intersect` メソッドは、指定されたコレクションにも存在するすべてのモデルを返します。

```php
use App\Models\User;

$users = $users->intersect(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-load"></a>
#### `load($relations)` {.collection-method}

`load` メソッドは、コレクション内のすべてのモデルの指定された関係を積極的に読み込みます。

```php
$users->load(['comments', 'posts']);

$users->load('comments.author');

$users->load(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-loadMissing"></a>
#### `loadMissing($relations)` {.collection-method}

`loadMissing` メソッドは、リレーションシップがまだロードされていない場合、コレクション内のすべてのモデルに対して指定されたリレーションシップを積極的にロードします。

```php
$users->loadMissing(['comments', 'posts']);

$users->loadMissing('comments.author');

$users->loadMissing(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-modelKeys"></a>
#### `modelKeys()` {.collection-method}

`modelKeys` メソッドは、コレクション内のすべてのモデルの主キーを返します。

```php
$users->modelKeys();

// [1, 2, 3, 4, 5]
```

<a name="method-makeVisible"></a>
#### `makeVisible($attributes)` {.collection-method}

通常、コレクション内の各モデルで「非表示」になる `makeVisible` メソッド [属性を可視化します](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json):

```php
$users = $users->makeVisible(['address', 'phone_number']);
```

<a name="method-makeHidden"></a>
#### `makeHidden($attributes)` {.collection-method}

通常、コレクション内の各モデルで「表示」される `makeHidden` メソッド [属性を非表示にする](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json):

```php
$users = $users->makeHidden(['address', 'phone_number']);
```

<a name="method-mergeVisible"></a>
#### `mergeVisible($attributes)` {.collection-method}

既存の表示属性を保持したままの `mergeVisible` メソッド [追加の属性を表示します](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json):

```php
$users = $users->mergeVisible(['middle_name']);
```

<a name="method-mergeHidden"></a>
#### `mergeHidden($attributes)` {.collection-method}

既存の非表示属性を保持したままの `mergeHidden` メソッド [追加の属性を非表示にします](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json):

```php
$users = $users->mergeHidden(['last_login_at']);
```

<a name="method-only"></a>
#### `only($keys)` {.collection-method}

`only` メソッドは、指定された主キーを持つすべてのモデルを返します。

```php
$users = $users->only([1, 2, 3]);
```

<a name="method-partition"></a>
#### `partition` {.collection-method}

`partition` メソッドは、`Illuminate\Database\Eloquent\Collection` コレクション インスタンスを含む `Illuminate\Support\Collection` のインスタンスを返します。

```php
$partition = $users->partition(fn ($user) => $user->age > 18);

dump($partition::class);    // Illuminate\Support\Collection
dump($partition[0]::class); // Illuminate\Database\Eloquent\Collection
dump($partition[1]::class); // Illuminate\Database\Eloquent\Collection
```

<a name="method-setAppends"></a>
#### `setAppends($attributes)` {.collection-method}

`setAppends` メソッドは、コレクション内の各モデルのすべての [追加された属性](/docs/{{version}}/eloquent-serialization#appending-values-to-json) を一時的にオーバーライドします。

```php
$users = $users->setAppends(['is_admin']);
```

<a name="method-setVisible"></a>
#### `setVisible($attributes)` {.collection-method}

`setVisible` メソッド [一時的に上書きする](/docs/{{version}}/eloquent-serialization#temporarily-modifying-attribute-visibility) コレクション内の各モデルに表示されるすべての属性:

```php
$users = $users->setVisible(['id', 'name']);
```

<a name="method-setHidden"></a>
#### `setHidden($attributes)` {.collection-method}

`setHidden` メソッド [一時的に上書きする](/docs/{{version}}/eloquent-serialization#temporarily-modifying-attribute-visibility) コレクション内の各モデルのすべての非表示属性:

```php
$users = $users->setHidden(['email', 'password', 'remember_token']);
```

<a name="method-toquery"></a>
#### `toQuery()` {.collection-method}

`toQuery` メソッドは、コレクション モデルの主キーに対する `whereIn` 制約を含む Eloquent クエリビルダ インスタンスを返します。

```php
use App\Models\User;

$users = User::where('status', 'VIP')->get();

$users->toQuery()->update([
    'status' => 'Administrator',
]);
```

<a name="method-unique"></a>
#### `unique($key = null, $strict = false)` {.collection-method}

`unique` メソッドは、コレクション内のすべての一意のモデルを返します。コレクション内の別のモデルと同じ主キーを持つモデルはすべて削除されます。

```php
$users = $users->unique();
```

<a name="method-withoutAppends"></a>
#### `withoutAppends()` {.collection-method}

`withoutAppends` メソッドは、コレクション内の各モデルのすべての [追加された属性](/docs/{{version}}/eloquent-serialization#appending-values-to-json) を一時的に削除します。

```php
$users = $users->withoutAppends();
```

<a name="custom-collections"></a>
## カスタムコレクション (Custom Collections)

特定のモデルと対話するときにカスタム `Collection` オブジェクトを使用したい場合は、モデルに `CollectedBy` 属性を追加できます。

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

あるいは、モデルに `newCollection` メソッドを定義することもできます。

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

`newCollection` メソッドを定義するか、モデルに `CollectedBy` 属性を追加すると、Eloquent が通常 `Illuminate\Database\Eloquent\Collection` インスタンスを返すときはいつでも、カスタム コレクションのインスタンスを受け取ることができます。

アプリケーション内のすべてのモデルにカスタム コレクションを使用したい場合は、アプリケーションのすべてのモデルによって拡張される基本モデル クラスで `newCollection` メソッドを定義する必要があります。

