<!-- # Eloquent: Collections -->
# Eloquent: Collections

- [Introduction](#introduction)
- [Available Methods](#available-methods)
- [Custom Collections](#custom-collections)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- All Eloquent methods that return more than one model result will return instances of the `Illuminate\Database\Eloquent\Collection` class, including results retrieved via the `get` method or accessed via a relationship. The Eloquent collection object extends Laravel's [base collection](/docs/10.x/collections), so it naturally inherits dozens of methods used to fluently work with the underlying array of Eloquent models. Be sure to review the Laravel collection documentation to learn all about these helpful methods! -->
複数のモデル結果を返すすべての Eloquent メソッドは、`get` メソッドを介して取得された結果やリレーションシップを介してアクセスされた結果を含む、`Illuminate\Database\Eloquent\Collection` クラスのインスタンスを返します。 Eloquent コレクション オブジェクトは Laravel の [base collection](/docs/10.x/collections) を拡張するため、基礎となる Eloquent モデルの配列をスムーズに操作するために使用される多数のメソッドを自然に継承します。これらの便利なメソッドについて詳しく知るには、必ず Laravel コレクションのドキュメントを参照してください。

<!-- All collections also serve as iterators, allowing you to loop over them as if they were simple PHP arrays: -->
すべてのコレクションはイテレータとしても機能するため、単純な PHP 配列であるかのようにループすることができます。

```
use App\Models\User;

$users = User::where('active', 1)->get();

foreach ($users as $user) {
    echo $user->name;
}
```

<!-- However, as previously mentioned, collections are much more powerful than arrays and expose a variety of map / reduce operations that may be chained using an intuitive interface. For example, we may remove all inactive models and then gather the first name for each remaining user: -->
ただし、前述したように、コレクションは配列よりもはるかに強力で、直感的なインターフェイスを使用して連鎖できるさまざまなマップ/リデュース操作を公開します。たとえば、非アクティブなモデルをすべて削除し、残りの各ユーザーの名を収集します。

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

<!-- While most Eloquent collection methods return a new instance of an Eloquent collection, the `collapse`, `flatten`, `flip`, `keys`, `pluck`, and `zip` methods return a [base collection](/docs/10.x/collections) instance. Likewise, if a `map` operation returns a collection that does not contain any Eloquent models, it will be converted to a base collection instance. -->
ほとんどの Eloquent コレクション メソッドは Eloquent コレクションの新しいインスタンスを返しますが、`collapse`、`flatten`、`flip`、`keys`、`pluck`、および `zip` メソッドは [base collection](/docs/10.x/collections) インスタンスを返します。同様に、`map` オペレーションが Eloquent モデルを含まないコレクションを返す場合、それはベース コレクション インスタンスに変換されます。

<a name="available-methods"></a>
<!-- ## Available Methods -->
## Available Methods

<!-- All Eloquent collections extend the base [Laravel collection](/docs/10.x/collections#available-methods) object; therefore, they inherit all of the powerful methods provided by the base collection class. -->
すべての Eloquent コレクションは、基本 [Laravel collection](/docs/10.x/collections#available-methods) オブジェクトを拡張します。したがって、これらは、基本コレクション クラスによって提供される強力なメソッドをすべて継承します。

<!-- In addition, the `Illuminate\Database\Eloquent\Collection` class provides a superset of methods to aid with managing your model collections. Most methods return `Illuminate\Database\Eloquent\Collection` instances; however, some methods, like `modelKeys`, return an `Illuminate\Support\Collection` instance. -->
さらに、`Illuminate\Database\Eloquent\Collection` クラスは、モデル コレクションの管理を支援するメソッドのスーパーセットを提供します。ほとんどのメソッドは `Illuminate\Database\Eloquent\Collection` インスタンスを返します。ただし、`modelKeys` などの一部のメソッドは、`Illuminate\Support\Collection` インスタンスを返します。

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[append](#method-append)
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
<!-- The `append` method may be used to indicate that an attribute should be [appended](/docs/10.x/eloquent-serialization#appending-values-to-json) for every model in the collection. This method accepts an array of attributes or a single attribute: -->
`append` メソッドを使用して、コレクション内のすべてのモデルの属性が [appended](/docs/10.x/eloquent-serialization#appending-values-to-json) である必要があることを示すことができます。このメソッドは、属性の配列または単一の属性を受け入れます。

```
$users->append('team');

$users->append(['team', 'is_admin']);
```

<a name="method-contains"></a>
<!-- #### `contains($key, $operator = null, $value = null)` -->
#### `contains($key, $operator = null, $value = null)`
<!-- The `contains` method may be used to determine if a given model instance is contained by the collection. This method accepts a primary key or a model instance: -->
`contains` メソッドは、特定のモデル インスタンスがコレクションに含まれているかどうかを判断するために使用できます。このメソッドは主キーまたはモデル インスタンスを受け入れます。

```
$users->contains(1);

$users->contains(User::find(1));
```

<a name="method-diff"></a>
<!-- #### `diff($items)` -->
#### `diff($items)`
<!-- The `diff` method returns all of the models that are not present in the given collection: -->
`diff` メソッドは、指定されたコレクションに存在しないすべてのモデルを返します。

```
use App\Models\User;

$users = $users->diff(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-except"></a>
<!-- #### `except($keys)` -->
#### `except($keys)`
<!-- The `except` method returns all of the models that do not have the given primary keys: -->
`except` メソッドは、指定された主キーを持たないすべてのモデルを返します。

```
$users = $users->except([1, 2, 3]);
```

<a name="method-find"></a>
<!-- #### `find($key)` -->
#### `find($key)`
<!-- The `find` method returns the model that has a primary key matching the given key. If `$key` is a model instance, `find` will attempt to return a model matching the primary key. If `$key` is an array of keys, `find` will return all models which have a primary key in the given array: -->
`find` メソッドは、指定されたキーに一致する主キーを持つモデルを返します。 `$key` がモデル インスタンスの場合、`find` は主キーに一致するモデルを返そうとします。 `$key` がキーの配列の場合、`find` は指定された配列に主キーを持つすべてのモデルを返します。

```
$users = User::all();

$user = $users->find(1);
```

<a name="method-fresh"></a>
<!-- #### `fresh($with = [])` -->
#### `fresh($with = [])`
<!-- The `fresh` method retrieves a fresh instance of each model in the collection from the database. In addition, any specified relationships will be eager loaded: -->
`fresh` メソッドは、コレクション内の各モデルの新しいインスタンスをデータベースから取得します。さらに、指定された関係はすべて積極的にロードされます。

```
$users = $users->fresh();

$users = $users->fresh('comments');
```

<a name="method-intersect"></a>
<!-- #### `intersect($items)` -->
#### `intersect($items)`
<!-- The `intersect` method returns all of the models that are also present in the given collection: -->
`intersect` メソッドは、指定されたコレクションにも存在するすべてのモデルを返します。

```
use App\Models\User;

$users = $users->intersect(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-load"></a>
<!-- #### `load($relations)` -->
#### `load($relations)`
<!-- The `load` method eager loads the given relationships for all models in the collection: -->
`load` メソッドは、コレクション内のすべてのモデルの指定された関係を積極的に読み込みます。

```
$users->load(['comments', 'posts']);

$users->load('comments.author');

$users->load(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-loadMissing"></a>
<!-- #### `loadMissing($relations)` -->
#### `loadMissing($relations)`
<!-- The `loadMissing` method eager loads the given relationships for all models in the collection if the relationships are not already loaded: -->
`loadMissing` メソッドは、リレーションシップがまだロードされていない場合、コレクション内のすべてのモデルに対して指定されたリレーションシップを積極的にロードします。

```
$users->loadMissing(['comments', 'posts']);

$users->loadMissing('comments.author');

$users->loadMissing(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-modelKeys"></a>
<!-- #### `modelKeys()` -->
#### `modelKeys()`
<!-- The `modelKeys` method returns the primary keys for all models in the collection: -->
`modelKeys` メソッドは、コレクション内のすべてのモデルの主キーを返します。

```
$users->modelKeys();

// [1, 2, 3, 4, 5]
```

<a name="method-makeVisible"></a>
<!-- #### `makeVisible($attributes)` -->
#### `makeVisible($attributes)`
<!-- The `makeVisible` method [makes attributes visible](/docs/10.x/eloquent-serialization#hiding-attributes-from-json) that are typically "hidden" on each model in the collection: -->
`makeVisible` メソッドは、通常コレクション内の各モデルで「非表示」になっている[makes attributes visible](/docs/10.x/eloquent-serialization#hiding-attributes-from-json):

```
$users = $users->makeVisible(['address', 'phone_number']);
```

<a name="method-makeHidden"></a>
<!-- #### `makeHidden($attributes)` -->
#### `makeHidden($attributes)`
<!-- The `makeHidden` method [hides attributes](/docs/10.x/eloquent-serialization#hiding-attributes-from-json) that are typically "visible" on each model in the collection: -->
`makeHidden` メソッドは、通常コレクション内の各モデルで「表示」されている[hides attributes](/docs/10.x/eloquent-serialization#hiding-attributes-from-json):

```
$users = $users->makeHidden(['address', 'phone_number']);
```

<a name="method-only"></a>
<!-- #### `only($keys)` -->
#### `only($keys)`
<!-- The `only` method returns all of the models that have the given primary keys: -->
`only` メソッドは、指定された主キーを持つすべてのモデルを返します。

```
$users = $users->only([1, 2, 3]);
```

<a name="method-setVisible"></a>
<!-- #### `setVisible($attributes)` -->
#### `setVisible($attributes)`
<!-- The `setVisible` method [temporarily overrides](/docs/10.x/eloquent-serialization#temporarily-modifying-attribute-visibility) all of the visible attributes on each model in the collection: -->
`setVisible` メソッドは、コレクション内の各モデルのすべての表示属性を[temporarily overrides](/docs/10.x/eloquent-serialization#temporarily-modifying-attribute-visibility):

```
$users = $users->setVisible(['id', 'name']);
```

<a name="method-setHidden"></a>
<!-- #### `setHidden($attributes)` -->
#### `setHidden($attributes)`
<!-- The `setHidden` method [temporarily overrides](/docs/10.x/eloquent-serialization#temporarily-modifying-attribute-visibility) all of the hidden attributes on each model in the collection: -->
`setHidden` メソッドは、コレクション内の各モデルのすべての非表示属性を[temporarily overrides](/docs/10.x/eloquent-serialization#temporarily-modifying-attribute-visibility):

```
$users = $users->setHidden(['email', 'password', 'remember_token']);
```

<a name="method-toquery"></a>
<!-- #### `toQuery()` -->
#### `toQuery()`
<!-- The `toQuery` method returns an Eloquent query builder instance containing a `whereIn` constraint on the collection model's primary keys: -->
`toQuery` メソッドは、コレクション モデルの主キーに対する `whereIn` 制約を含む Eloquent クエリビルダ インスタンスを返します。

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
`unique` メソッドは、コレクション内のすべての一意のモデルを返します。コレクション内の別のモデルと同じ主キーを持つ同じタイプのモデルはすべて削除されます。

```
$users = $users->unique();
```

<a name="custom-collections"></a>
<!-- ## Custom Collections -->
## Custom Collections

<!-- If you would like to use a custom `Collection` object when interacting with a given model, you may define a `newCollection` method on your model: -->
特定のモデルと対話するときにカスタム `Collection` オブジェクトを使用したい場合は、モデルに `newCollection` メソッドを定義できます。

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

<!-- Once you have defined a `newCollection` method, you will receive an instance of your custom collection anytime Eloquent would normally return an `Illuminate\Database\Eloquent\Collection` instance. If you would like to use a custom collection for every model in your application, you should define the `newCollection` method on a base model class that is extended by all of your application's models. -->
`newCollection` メソッドを定義すると、Eloquent が通常 `Illuminate\Database\Eloquent\Collection` インスタンスを返すときはいつでも、カスタム コレクションのインスタンスを受け取ることができます。アプリケーション内のすべてのモデルにカスタム コレクションを使用したい場合は、アプリケーションのすべてのモデルによって拡張される基本モデル クラスで `newCollection` メソッドを定義する必要があります。

