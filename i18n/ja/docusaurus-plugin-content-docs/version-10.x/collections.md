# コレクション (Collections)

- [Introduction](#introduction)
    - [コレクションの作成](#creating-collections)
    - [コレクションの拡張](#extending-collections)
- [利用可能な方法](#available-methods)
- [高次メッセージ](#higher-order-messages)
- [レイジーコレクション](#lazy-collections)
    - [Introduction](#lazy-collection-introduction)
    - [遅延コレクションの作成](#creating-lazy-collections)
    - [数え切れないほどの契約](#the-enumerable-contract)
    - [遅延収集メソッド](#lazy-collection-methods)

<a name="introduction"></a>
## 導入 (Introduction)

`Illuminate\Support\Collection` クラスは、データの配列を操作するための流暢で便利なラッパーを提供します。たとえば、次のコードを確認してください。 `collect` ヘルパを使用して配列から新しいコレクション インスタンスを作成し、各要素に対して `strtoupper` 関数を実行して、空の要素をすべて削除します。

    $collection = collect(['taylor', 'abigail', null])->map(function (?string $name) {
        return strtoupper($name);
    })->reject(function (string $name) {
        return empty($name);
    });

ご覧のとおり、`Collection` クラスを使用すると、そのメソッドを連鎖させて、基になる配列のスムーズなマッピングと削減を実行できます。一般に、コレクションは不変です。つまり、すべての `Collection` メソッドはまったく新しい `Collection` インスタンスを返します。

<a name="creating-collections"></a>
### コレクションの作成

前述したように、`collect` ヘルパは、指定された配列の新しい `Illuminate\Support\Collection` インスタンスを返します。したがって、コレクションの作成は次のように簡単です。

    $collection = collect([1, 2, 3]);

> [!NOTE]  
> [Eloquent](/docs/{{version}}/eloquent) クエリの結果は、常に `Collection` インスタンスとして返されます。

<a name="extending-collections"></a>
### コレクションの拡張

コレクションは「マクロ可能」であるため、実行時に `Collection` クラスにメソッドを追加できます。 `Illuminate\Support\Collection` クラスの `macro` メソッドは、マクロが呼び出されたときに実行されるクロージャを受け入れます。マクロ クロージャは、あたかもコレクション クラスの実際のメソッドであるかのように、`$this` を介してコレクションの他のメソッドにアクセスできます。たとえば、次のコードは、`toUpper` メソッドを `Collection` クラスに追加します。

    use Illuminate\Support\Collection;
    use Illuminate\Support\Str;

    Collection::macro('toUpper', function () {
        return $this->map(function (string $value) {
            return Str::upper($value);
        });
    });

    $collection = collect(['first', 'second']);

    $upper = $collection->toUpper();

    // ['FIRST', 'SECOND']

通常、コレクション マクロは、[サービスプロバイダ](/docs/{{version}}/providers) の `boot` メソッドで宣言する必要があります。

<a name="macro-arguments"></a>
#### マクロ引数

必要に応じて、追加の引数を受け入れるマクロを定義できます。

    use Illuminate\Support\Collection;
    use Illuminate\Support\Facades\Lang;

    Collection::macro('toLocale', function (string $locale) {
        return $this->map(function (string $value) use ($locale) {
            return Lang::get($value, [], $locale);
        });
    });

    $collection = collect(['first', 'second']);

    $translated = $collection->toLocale('es');

<a name="available-methods"></a>
## 利用可能な方法 (Available Methods)

残りのコレクションのドキュメントの大部分では、`Collection` クラスで使用できる各メソッドについて説明します。これらのメソッドはすべて、基礎となる配列をスムーズに操作するために連鎖させることができることに注意してください。さらに、ほぼすべてのメソッドは新しい `Collection` インスタンスを返すため、必要に応じてコレクションの元のコピーを保存できます。

<style>
    .collection-method-list > p {
        columns: 10.8em 3; -moz-columns: 10.8em 3; -webkit-columns: 10.8em 3;
    }

    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
</style>

<div class="collection-method-list" markdown="1">

[all](#method-all)
[average](#method-average)
[avg](#method-avg)
[chunk](#method-chunk)
[chunkWhile](#method-chunkwhile)
[collapse](#method-collapse)
[collect](#method-collect)
[combine](#method-combine)
[concat](#method-concat)
[contains](#method-contains)
[containsOneItem](#method-containsoneitem)
[containsStrict](#method-containsstrict)
[count](#method-count)
[countBy](#method-countBy)
[crossJoin](#method-crossjoin)
[dd](#method-dd)
[diff](#method-diff)
[diffAssoc](#method-diffassoc)
[diffAssocUsing](#method-diffassocusing)
[diffKeys](#method-diffkeys)
[doesntContain](#method-doesntcontain)
[dot](#method-dot)
[dump](#method-dump)
[duplicates](#method-duplicates)
[duplicatesStrict](#method-duplicatesstrict)
[each](#method-each)
[eachSpread](#method-eachspread)
[ensure](#method-ensure)
[every](#method-every)
[except](#method-except)
[filter](#method-filter)
[first](#method-first)
[firstOrFail](#method-first-or-fail)
[firstWhere](#method-first-where)
[flatMap](#method-flatmap)
[flatten](#method-flatten)
[flip](#method-flip)
[forget](#method-forget)
[forPage](#method-forpage)
[get](#method-get)
[groupBy](#method-groupby)
[has](#method-has)
[hasAny](#method-hasany)
[implode](#method-implode)
[intersect](#method-intersect)
[intersectAssoc](#method-intersectAssoc)
[intersectByKeys](#method-intersectbykeys)
[isEmpty](#method-isempty)
[isNotEmpty](#method-isnotempty)
[join](#method-join)
[keyBy](#method-keyby)
[keys](#method-keys)
[last](#method-last)
[lazy](#method-lazy)
[macro](#method-macro)
[make](#method-make)
[map](#method-map)
[mapInto](#method-mapinto)
[mapSpread](#method-mapspread)
[mapToGroups](#method-maptogroups)
[mapWithKeys](#method-mapwithkeys)
[max](#method-max)
[median](#method-median)
[merge](#method-merge)
[mergeRecursive](#method-mergerecursive)
[min](#method-min)
[mode](#method-mode)
[nth](#method-nth)
[only](#method-only)
[pad](#method-pad)
[partition](#method-partition)
[percentage](#method-percentage)
[pipe](#method-pipe)
[pipeInto](#method-pipeinto)
[pipeThrough](#method-pipethrough)
[pluck](#method-pluck)
[pop](#method-pop)
[prepend](#method-prepend)
[pull](#method-pull)
[push](#method-push)
[put](#method-put)
[random](#method-random)
[range](#method-range)
[reduce](#method-reduce)
[reduceSpread](#method-reduce-spread)
[reject](#method-reject)
[replace](#method-replace)
[replaceRecursive](#method-replacerecursive)
[reverse](#method-reverse)
[search](#method-search)
[select](#method-select)
[shift](#method-shift)
[shuffle](#method-shuffle)
[skip](#method-skip)
[skipUntil](#method-skipuntil)
[skipWhile](#method-skipwhile)
[slice](#method-slice)
[sliding](#method-sliding)
[sole](#method-sole)
[some](#method-some)
[sort](#method-sort)
[sortBy](#method-sortby)
[sortByDesc](#method-sortbydesc)
[sortDesc](#method-sortdesc)
[sortKeys](#method-sortkeys)
[sortKeysDesc](#method-sortkeysdesc)
[sortKeysUsing](#method-sortkeysusing)
[splice](#method-splice)
[split](#method-split)
[splitIn](#method-splitin)
[sum](#method-sum)
[take](#method-take)
[takeUntil](#method-takeuntil)
[takeWhile](#method-takewhile)
[tap](#method-tap)
[times](#method-times)
[toArray](#method-toarray)
[toJson](#method-tojson)
[transform](#method-transform)
[undot](#method-undot)
[union](#method-union)
[unique](#method-unique)
[uniqueStrict](#method-uniquestrict)
[unless](#method-unless)
[unlessEmpty](#method-unlessempty)
[unlessNotEmpty](#method-unlessnotempty)
[unwrap](#method-unwrap)
[value](#method-value)
[values](#method-values)
[when](#method-when)
[whenEmpty](#method-whenempty)
[whenNotEmpty](#method-whennotempty)
[where](#method-where)
[whereStrict](#method-wherestrict)
[whereBetween](#method-wherebetween)
[whereIn](#method-wherein)
[whereInStrict](#method-whereinstrict)
[whereInstanceOf](#method-whereinstanceof)
[whereNotBetween](#method-wherenotbetween)
[whereNotIn](#method-wherenotin)
[whereNotInStrict](#method-wherenotinstrict)
[whereNotNull](#method-wherenotnull)
[whereNull](#method-wherenull)
[wrap](#method-wrap)
[zip](#method-zip)

</div>

<a name="method-listing"></a>
## メソッドリスト (Method Listing)

<style>
    .collection-method code {
        font-size: 14px;
    }

    .collection-method:not(.first-collection-method) {
        margin-top: 50px;
    }
</style>

<a name="method-all"></a>
#### `all()` {.collection-method .first-collection-method}

`all` メソッドは、コレクションによって表される基になる配列を返します。

    collect([1, 2, 3])->all();

    // [1, 2, 3]

<a name="method-average"></a>
#### `average()` {.collection-method}

[`avg`](#method-avg) メソッドのエイリアス。

<a name="method-avg"></a>
#### `avg()` {.collection-method}

`avg` メソッドは、指定されたキーの [平均値](https://en.wikipedia.org/wiki/Average) を返します。

    $average = collect([
        ['foo' => 10],
        ['foo' => 10],
        ['foo' => 20],
        ['foo' => 40]
    ])->avg('foo');

    // 20

    $average = collect([1, 1, 2, 4])->avg();

    // 2

<a name="method-chunk"></a>
#### `chunk()` {.collection-method}

`chunk` メソッドは、コレクションを指定されたサイズの複数の小さなコレクションに分割します。

    $collection = collect([1, 2, 3, 4, 5, 6, 7]);

    $chunks = $collection->chunk(4);

    $chunks->all();

    // [[1, 2, 3, 4], [5, 6, 7]]

この方法は、[Bootstrap](/docs/{{version}}/views) などのグリッド システムを操作する場合、[views](https://getbootstrap.com/docs/4.1/layout/grid/) で特に便利です。たとえば、グリッドに表示したい [Eloquent](/docs/{{version}}/eloquent) モデルのコレクションがあるとします。

```blade
@foreach ($products->chunk(3) as $chunk)
    <div class="row">
        @foreach ($chunk as $product)
            <div class="col-xs-4">{{ $product->name }}</div>
        @endforeach
    </div>
@endforeach
```

<a name="method-chunkwhile"></a>
#### `chunkWhile()` {.collection-method}

`chunkWhile` メソッドは、指定されたコールバックの評価に基づいて、コレクションを複数の小さなコレクションに分割します。クロージャに渡される `$chunk` 変数は、前の要素を検査するために使用できます。

    $collection = collect(str_split('AABBCCCD'));

    $chunks = $collection->chunkWhile(function (string $value, int $key, Collection $chunk) {
        return $value === $chunk->last();
    });

    $chunks->all();

    // [['A', 'A'], ['B', 'B'], ['C', 'C', 'C'], ['D']]

<a name="method-collapse"></a>
#### `collapse()` {.collection-method}

`collapse` メソッドは、配列のコレクションを単一のフラットなコレクションに折りたたみます。

    $collection = collect([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]);

    $collapsed = $collection->collapse();

    $collapsed->all();

    // [1, 2, 3, 4, 5, 6, 7, 8, 9]

<a name="method-collect"></a>
#### `collect()` {.collection-method}

`collect` メソッドは、現在コレクション内の項目を含む新しい `Collection` インスタンスを返します。

    $collectionA = collect([1, 2, 3]);

    $collectionB = $collectionA->collect();

    $collectionB->all();

    // [1, 2, 3]

`collect` メソッドは、主に [怠惰なコレクション](#lazy-collections) を標準の `Collection` インスタンスに変換する場合に役立ちます。

    $lazyCollection = LazyCollection::make(function () {
        yield 1;
        yield 2;
        yield 3;
    });

    $collection = $lazyCollection->collect();

    $collection::class;

    // 'Illuminate\Support\Collection'

    $collection->all();

    // [1, 2, 3]

> [!NOTE]  
> `collect` メソッドは、`Enumerable` のインスタンスがあり、非遅延コレクション インスタンスが必要な場合に特に便利です。 `collect()` は `Enumerable` コントラクトの一部であるため、これを安全に使用して `Collection` インスタンスを取得できます。

<a name="method-combine"></a>
#### `combine()` {.collection-method}

`combine` メソッドは、コレクションの値をキーとして、別の配列またはコレクションの値と組み合わせます。

    $collection = collect(['name', 'age']);

    $combined = $collection->combine(['George', 29]);

    $combined->all();

    // ['name' => 'George', 'age' => 29]

<a name="method-concat"></a>
#### `concat()` {.collection-method}

`concat` メソッドは、指定された `array` またはコレクションの値を別のコレクションの末尾に追加します。

    $collection = collect(['John Doe']);

    $concatenated = $collection->concat(['Jane Doe'])->concat(['name' => 'Johnny Doe']);

    $concatenated->all();

    // ['John Doe', 'Jane Doe', 'Johnny Doe']

`concat` メソッドは、元のコレクションに連結された項目のキーを数値的に再インデックスします。連想コレクション内のキーを維持するには、[merge](#method-merge) メソッドを参照してください。

<a name="method-contains"></a>
#### `contains()` {.collection-method}

`contains` メソッドは、コレクションに特定の項目が含まれているかどうかを判断します。クロージャを `contains` メソッドに渡して、指定された真理値テストに一致する要素がコレクション内に存在するかどうかを判断できます。

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->contains(function (int $value, int $key) {
        return $value > 5;
    });

    // false

あるいは、文字列を `contains` メソッドに渡して、コレクションに特定の項目値が含まれているかどうかを判断することもできます。

    $collection = collect(['name' => 'Desk', 'price' => 100]);

    $collection->contains('Desk');

    // true

    $collection->contains('New York');

    // false

キーと値のペアを `contains` メソッドに渡すこともできます。これにより、指定されたペアがコレクション内に存在するかどうかが判断されます。

    $collection = collect([
        ['product' => 'Desk', 'price' => 200],
        ['product' => 'Chair', 'price' => 100],
    ]);

    $collection->contains('product', 'Bookcase');

    // false

`contains` メソッドは、項目値をチェックするときに「緩やかな」比較を使用します。つまり、整数値を持つ文字列は、同じ値の整数と等しいと見なされます。 「厳密な」比較を使用してフィルタリングするには、[`containsStrict`](#method-containsstrict) メソッドを使用します。

`contains` の逆については、[doesntContain](#method-doesntcontain) メソッドを参照してください。

<a name="method-containsoneitem"></a>
#### `containsOneItem()` {.collection-method}

`containsOneItem` メソッドは、コレクションに単一の項目が含まれているかどうかを判断します。

    collect([])->containsOneItem();

    // false

    collect(['1'])->containsOneItem();

    // true

    collect(['1', '2'])->containsOneItem();

    // false

<a name="method-containsstrict"></a>
#### `containsStrict()` {.collection-method}

このメソッドには、[`contains`](#method-contains) メソッドと同じシグネチャがあります。ただし、すべての値は「厳密な」比較を使用して比較されます。

> [!NOTE]  
> [Eloquent コレクション](/docs/{{version}}/eloquent-collections#method-contains) を使用すると、このメソッドの動作が変更されます。

<a name="method-count"></a>
#### `count()` {.collection-method}

`count` メソッドは、コレクション内の項目の合計数を返します。

    $collection = collect([1, 2, 3, 4]);

    $collection->count();

    // 4

<a name="method-countBy"></a>
#### `countBy()` {.collection-method}

`countBy` メソッドは、コレクション内の値の出現をカウントします。デフォルトでは、このメソッドはすべての要素の出現をカウントするため、コレクション内の要素の特定の「タイプ」をカウントできます。

    $collection = collect([1, 2, 2, 2, 3]);

    $counted = $collection->countBy();

    $counted->all();

    // [1 => 1, 2 => 3, 3 => 1]

カスタム値ですべての項目をカウントするには、クロージャを `countBy` メソッドに渡します。

    $collection = collect(['alice@gmail.com', 'bob@yahoo.com', 'carlos@gmail.com']);

    $counted = $collection->countBy(function (string $email) {
        return substr(strrchr($email, "@"), 1);
    });

    $counted->all();

    // ['gmail.com' => 2, 'yahoo.com' => 1]

<a name="method-crossjoin"></a>
#### `crossJoin()` {.collection-method}

`crossJoin` メソッドは、指定された配列またはコレクション間でコレクションの値を交差結合し、すべての可能な順列を含むデカルト積を返します。

    $collection = collect([1, 2]);

    $matrix = $collection->crossJoin(['a', 'b']);

    $matrix->all();

    /*
        [
            [1, 'a'],
            [1, 'b'],
            [2, 'a'],
            [2, 'b'],
        ]
    */

    $collection = collect([1, 2]);

    $matrix = $collection->crossJoin(['a', 'b'], ['I', 'II']);

    $matrix->all();

    /*
        [
            [1, 'a', 'I'],
            [1, 'a', 'II'],
            [1, 'b', 'I'],
            [1, 'b', 'II'],
            [2, 'a', 'I'],
            [2, 'a', 'II'],
            [2, 'b', 'I'],
            [2, 'b', 'II'],
        ]
    */

<a name="method-dd"></a>
#### `dd()` {.collection-method}

`dd` メソッドは、コレクションのアイテムをダンプし、スクリプトの実行を終了します。

    $collection = collect(['John Doe', 'Jane Doe']);

    $collection->dd();

    /*
        Collection {
            #items: array:2 [
                0 => "John Doe"
                1 => "Jane Doe"
            ]
        }
    */

スクリプトの実行を停止したくない場合は、代わりに [`dump`](#method-dump) メソッドを使用してください。

<a name="method-diff"></a>
#### `diff()` {.collection-method}

`diff` メソッドは、その値に基づいて、コレクションを別のコレクションまたはプレーンな PHP `array` と比較します。このメソッドは、指定されたコレクションに存在しない元のコレクションの値を返します。

    $collection = collect([1, 2, 3, 4, 5]);

    $diff = $collection->diff([2, 4, 6, 8]);

    $diff->all();

    // [1, 3, 5]

> [!NOTE]  
> [Eloquent コレクション](/docs/{{version}}/eloquent-collections#method-diff) を使用すると、このメソッドの動作が変更されます。

<a name="method-diffassoc"></a>
#### `diffAssoc()` {.collection-method}

`diffAssoc` メソッドは、キーと値に基づいてコレクションを別のコレクションまたはプレーン PHP `array` と比較します。このメソッドは、指定されたコレクションに存在しない、元のコレクション内のキーと値のペアを返します。

    $collection = collect([
        'color' => 'orange',
        'type' => 'fruit',
        'remain' => 6,
    ]);

    $diff = $collection->diffAssoc([
        'color' => 'yellow',
        'type' => 'fruit',
        'remain' => 3,
        'used' => 6,
    ]);

    $diff->all();

    // ['color' => 'orange', 'remain' => 6]

<a name="method-diffassocusing"></a>
#### `diffAssocUsing()` {.collection-method}

`diffAssoc` とは異なり、`diffAssocUsing` はインデックス比較のためにユーザー指定のコールバック関数を受け入れます。

    $collection = collect([
        'color' => 'orange',
        'type' => 'fruit',
        'remain' => 6,
    ]);

    $diff = $collection->diffAssocUsing([
        'Color' => 'yellow',
        'Type' => 'fruit',
        'Remain' => 3,
    ], 'strnatcasecmp');

    $diff->all();

    // ['color' => 'orange', 'remain' => 6]

コールバックは、ゼロ以下、ゼロ以上の整数を返す比較関数である必要があります。詳細については、[`array_diff_uassoc`](https://www.php.net/array_diff_uassoc#refsect1-function.array-diff-uassoc-parameters) に関する PHP ドキュメントを参照してください。これは、`diffAssocUsing` メソッドが内部で使用する PHP 関数です。

<a name="method-diffkeys"></a>
#### `diffKeys()` {.collection-method}

`diffKeys` メソッドは、キーに基づいてコレクションを別のコレクションまたはプレーン PHP `array` と比較します。このメソッドは、指定されたコレクションに存在しない、元のコレクション内のキーと値のペアを返します。

    $collection = collect([
        'one' => 10,
        'two' => 20,
        'three' => 30,
        'four' => 40,
        'five' => 50,
    ]);

    $diff = $collection->diffKeys([
        'two' => 2,
        'four' => 4,
        'six' => 6,
        'eight' => 8,
    ]);

    $diff->all();

    // ['one' => 10, 'three' => 30, 'five' => 50]

<a name="method-doesntcontain"></a>
#### `doesntContain()` {.collection-method}

`doesntContain` メソッドは、コレクションに特定の項目が含まれていないかどうかを判断します。クロージャを `doesntContain` メソッドに渡して、指定された真理値テストに一致する要素がコレクション内に存在するかどうかを判断できます。

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->doesntContain(function (int $value, int $key) {
        return $value < 5;
    });

    // false

あるいは、文字列を `doesntContain` メソッドに渡して、コレクションに特定の項目値が含まれていないかどうかを判断することもできます。

    $collection = collect(['name' => 'Desk', 'price' => 100]);

    $collection->doesntContain('Table');

    // true

    $collection->doesntContain('Desk');

    // false

キーと値のペアを `doesntContain` メソッドに渡すこともできます。これにより、指定されたペアがコレクションに存在しないかどうかが判断されます。

    $collection = collect([
        ['product' => 'Desk', 'price' => 200],
        ['product' => 'Chair', 'price' => 100],
    ]);

    $collection->doesntContain('product', 'Bookcase');

    // true

`doesntContain` メソッドは、項目値をチェックするときに「緩やかな」比較を使用します。つまり、整数値を持つ文字列は、同じ値の整数と等しいと見なされます。

<a name="method-dot"></a>
#### `dot()` {.collection-method}

`dot` メソッドは、多次元コレクションを、深さを示すために「ドット」表記を使用する単一レベルのコレクションに平坦化します。

    $collection = collect(['products' => ['desk' => ['price' => 100]]]);

    $flattened = $collection->dot();

    $flattened->all();

    // ['products.desk.price' => 100]

<a name="method-dump"></a>
#### `dump()` {.collection-method}

`dump` メソッドは、コレクションの項目をダンプします。

    $collection = collect(['John Doe', 'Jane Doe']);

    $collection->dump();

    /*
        Collection {
            #items: array:2 [
                0 => "John Doe"
                1 => "Jane Doe"
            ]
        }
    */

コレクションのダンプ後にスクリプトの実行を停止する場合は、代わりに [`dd`](#method-dd) メソッドを使用します。

<a name="method-duplicates"></a>
#### `duplicates()` {.collection-method}

`duplicates` メソッドは、コレクションから重複した値を取得して返します。

    $collection = collect(['a', 'b', 'a', 'c', 'b']);

    $collection->duplicates();

    // [2 => 'a', 4 => 'b']

コレクションに配列またはオブジェクトが含まれている場合は、重複値をチェックする属性のキーを渡すことができます。

    $employees = collect([
        ['email' => 'abigail@example.com', 'position' => 'Developer'],
        ['email' => 'james@example.com', 'position' => 'Designer'],
        ['email' => 'victoria@example.com', 'position' => 'Developer'],
    ]);

    $employees->duplicates('position');

    // [2 => 'Developer']

<a name="method-duplicatesstrict"></a>
#### `duplicatesStrict()` {.collection-method}

このメソッドには、[`duplicates`](#method-duplicates) メソッドと同じシグネチャがあります。ただし、すべての値は「厳密な」比較を使用して比較されます。

<a name="method-each"></a>
#### `each()` {.collection-method}

`each` メソッドは、コレクション内の項目を反復処理し、各項目をクロージャーに渡します。

    $collection = collect([1, 2, 3, 4]);

    $collection->each(function (int $item, int $key) {
        // ...
    });

項目の反復処理を停止したい場合は、クロージャから `false` を返すことができます。

    $collection->each(function (int $item, int $key) {
        if (/* condition */) {
            return false;
        }
    });

<a name="method-eachspread"></a>
#### `eachSpread()` {.collection-method}

`eachSpread` メソッドはコレクションの項目を反復処理し、ネストされた各項目の値を指定されたコールバックに渡します。

    $collection = collect([['John Doe', 35], ['Jane Doe', 33]]);

    $collection->eachSpread(function (string $name, int $age) {
        // ...
    });

コールバックから `false` を返すことで、項目の反復処理を停止できます。

    $collection->eachSpread(function (string $name, int $age) {
        return false;
    });

<a name="method-ensure"></a>
#### `ensure()` {.collection-method}

`ensure` メソッドは、コレクションのすべての要素が特定の型または型のリストであることを検証するために使用できます。それ以外の場合は、`UnexpectedValueException` がスローされます。

    return $collection->ensure(User::class);

    return $collection->ensure([User::class, Customer::class]);

`string`、`int`、`float`、`bool`、`array` などのプリミティブ タイプも指定できます。

    return $collection->ensure('int');

> [!WARNING]  
> `ensure` メソッドは、異なるタイプの要素が後でコレクションに追加されないことを保証しません。

<a name="method-every"></a>
#### `every()` {.collection-method}

`every` メソッドは、コレクションのすべての要素が指定された真理テストに合格することを検証するために使用できます。

    collect([1, 2, 3, 4])->every(function (int $value, int $key) {
        return $value > 2;
    });

    // false

コレクションが空の場合、`every` メソッドは true を返します。

    $collection = collect([]);

    $collection->every(function (int $value, int $key) {
        return $value > 2;
    });

    // true

<a name="method-except"></a>
#### `except()` {.collection-method}

`except` メソッドは、指定されたキーを持つアイテムを除く、コレクション内のすべてのアイテムを返します。

    $collection = collect(['product_id' => 1, 'price' => 100, 'discount' => false]);

    $filtered = $collection->except(['price', 'discount']);

    $filtered->all();

    // ['product_id' => 1]

`except` の逆については、[only](#method-only) メソッドを参照してください。

> [!NOTE]  
> [Eloquent コレクション](/docs/{{version}}/eloquent-collections#method-except) を使用すると、このメソッドの動作が変更されます。

<a name="method-filter"></a>
#### `filter()` {.collection-method}

`filter` メソッドは、指定されたコールバックを使用してコレクションをフィルタリングし、指定された真実テストに合格した項目のみを保持します。

    $collection = collect([1, 2, 3, 4]);

    $filtered = $collection->filter(function (int $value, int $key) {
        return $value > 2;
    });

    $filtered->all();

    // [3, 4]

コールバックが指定されていない場合は、`false` に相当するコレクションのすべてのエントリが削除されます。

    $collection = collect([1, 2, 3, null, false, '', 0, []]);

    $collection->filter()->all();

    // [1, 2, 3]

`filter` の逆については、[reject](#method-reject) メソッドを参照してください。

<a name="method-first"></a>
#### `first()` {.collection-method}

`first` メソッドは、指定された真理テストに合格したコレクション内の最初の要素を返します。

    collect([1, 2, 3, 4])->first(function (int $value, int $key) {
        return $value > 2;
    });

    // 3

引数なしで `first` メソッドを呼び出して、コレクションの最初の要素を取得することもできます。コレクションが空の場合、`null` が返されます。

    collect([1, 2, 3, 4])->first();

    // 1

<a name="method-first-or-fail"></a>
#### `firstOrFail()` {.collection-method}

`firstOrFail` メソッドは、`first` メソッドと同じです。ただし、結果が見つからない場合は、`Illuminate\Support\ItemNotFoundException` 例外がスローされます。

    collect([1, 2, 3, 4])->firstOrFail(function (int $value, int $key) {
        return $value > 5;
    });

    // Throws ItemNotFoundException...

引数なしで `firstOrFail` メソッドを呼び出して、コレクションの最初の要素を取得することもできます。コレクションが空の場合、`Illuminate\Support\ItemNotFoundException` 例外がスローされます。

    collect([])->firstOrFail();

    // Throws ItemNotFoundException...

<a name="method-first-where"></a>
#### `firstWhere()` {.collection-method}

`firstWhere` メソッドは、指定されたキーと値のペアを持つコレクション内の最初の要素を返します。

    $collection = collect([
        ['name' => 'Regena', 'age' => null],
        ['name' => 'Linda', 'age' => 14],
        ['name' => 'Diego', 'age' => 23],
        ['name' => 'Linda', 'age' => 84],
    ]);

    $collection->firstWhere('name', 'Linda');

    // ['name' => 'Linda', 'age' => 14]

比較演算子を使用して `firstWhere` メソッドを呼び出すこともできます。

    $collection->firstWhere('age', '>=', 18);

    // ['name' => 'Diego', 'age' => 23]

[where](#method-where) メソッドと同様に、`firstWhere` メソッドに 1 つの引数を渡すことができます。このシナリオでは、`firstWhere` メソッドは、指定された項目キーの値が「真実」である最初の項目を返します。

    $collection->firstWhere('age');

    // ['name' => 'Linda', 'age' => 14]

<a name="method-flatmap"></a>
#### `flatMap()` {.collection-method}

`flatMap` メソッドはコレクションを反復処理し、各値を指定されたクロージャに渡します。クロージャは自由に項目を変更して返すことができるため、変更された項目の新しいコレクションが形成されます。次に、配列は 1 レベル平坦化されます。

    $collection = collect([
        ['name' => 'Sally'],
        ['school' => 'Arkansas'],
        ['age' => 28]
    ]);

    $flattened = $collection->flatMap(function (array $values) {
        return array_map('strtoupper', $values);
    });

    $flattened->all();

    // ['name' => 'SALLY', 'school' => 'ARKANSAS', 'age' => '28'];

<a name="method-flatten"></a>
#### `flatten()` {.collection-method}

`flatten` メソッドは、多次元コレクションを単一次元にフラット化します。

    $collection = collect([
        'name' => 'taylor',
        'languages' => [
            'php', 'javascript'
        ]
    ]);

    $flattened = $collection->flatten();

    $flattened->all();

    // ['taylor', 'php', 'javascript'];

必要に応じて、`flatten` メソッドに「深さ」引数を渡すことができます。

    $collection = collect([
        'Apple' => [
            [
                'name' => 'iPhone 6S',
                'brand' => 'Apple'
            ],
        ],
        'Samsung' => [
            [
                'name' => 'Galaxy S7',
                'brand' => 'Samsung'
            ],
        ],
    ]);

    $products = $collection->flatten(1);

    $products->values()->all();

    /*
        [
            ['name' => 'iPhone 6S', 'brand' => 'Apple'],
            ['name' => 'Galaxy S7', 'brand' => 'Samsung'],
        ]
    */

この例では、深さを指定せずに `flatten` を呼び出すと、ネストされた配列もフラット化され、`['iPhone 6S', 'Apple', 'Galaxy S7', 'Samsung']` になります。深さを指定すると、ネストされた配列を平坦化するレベルの数を指定できます。

<a name="method-flip"></a>
#### `flip()` {.collection-method}

`flip` メソッドは、コレクションのキーを対応する値と交換します。

    $collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

    $flipped = $collection->flip();

    $flipped->all();

    // ['taylor' => 'name', 'laravel' => 'framework']

<a name="method-forget"></a>
#### `forget()` {.collection-method}

`forget` メソッドは、キーによってコレクションから項目を削除します。

    $collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

    $collection->forget('name');

    $collection->all();

    // ['framework' => 'laravel']

> [!WARNING]  
> 他のほとんどのコレクション メソッドとは異なり、`forget` は変更された新しいコレクションを返しません。呼び出されたコレクションを変更します。

<a name="method-forpage"></a>
#### `forPage()` {.collection-method}

`forPage` メソッドは、指定されたページ番号に存在する項目を含む新しいコレクションを返します。このメソッドは、最初の引数としてページ番号を受け入れ、2 番目の引数としてページごとに表示するアイテムの数を受け入れます。

    $collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9]);

    $chunk = $collection->forPage(2, 3);

    $chunk->all();

    // [4, 5, 6]

<a name="method-get"></a>
#### `get()` {.collection-method}

`get` メソッドは、指定されたキーの項目を返します。キーが存在しない場合は、`null` が返されます。

    $collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

    $value = $collection->get('name');

    // taylor

オプションで、デフォルト値を 2 番目の引数として渡すこともできます。

    $collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

    $value = $collection->get('age', 34);

    // 34

コールバックをメソッドのデフォルト値として渡すこともできます。指定されたキーが存在しない場合は、コールバックの結果が返されます。

    $collection->get('email', function () {
        return 'taylor@example.com';
    });

    // taylor@example.com

<a name="method-groupby"></a>
#### `groupBy()` {.collection-method}

`groupBy` メソッドは、指定されたキーによってコレクションの項目をグループ化します。

    $collection = collect([
        ['account_id' => 'account-x10', 'product' => 'Chair'],
        ['account_id' => 'account-x10', 'product' => 'Bookcase'],
        ['account_id' => 'account-x11', 'product' => 'Desk'],
    ]);

    $grouped = $collection->groupBy('account_id');

    $grouped->all();

    /*
        [
            'account-x10' => [
                ['account_id' => 'account-x10', 'product' => 'Chair'],
                ['account_id' => 'account-x10', 'product' => 'Bookcase'],
            ],
            'account-x11' => [
                ['account_id' => 'account-x11', 'product' => 'Desk'],
            ],
        ]
    */

文字列 `key` を渡す代わりに、コールバックを渡すこともできます。コールバックは、次のようにしてグループのキーとなる値を返す必要があります。

    $grouped = $collection->groupBy(function (array $item, int $key) {
        return substr($item['account_id'], -3);
    });

    $grouped->all();

    /*
        [
            'x10' => [
                ['account_id' => 'account-x10', 'product' => 'Chair'],
                ['account_id' => 'account-x10', 'product' => 'Bookcase'],
            ],
            'x11' => [
                ['account_id' => 'account-x11', 'product' => 'Desk'],
            ],
        ]
    */

複数のグループ化基準を配列として渡すことができます。各配列要素は、多次元配列内の対応するレベルに適用されます。

    $data = new Collection([
        10 => ['user' => 1, 'skill' => 1, 'roles' => ['Role_1', 'Role_3']],
        20 => ['user' => 2, 'skill' => 1, 'roles' => ['Role_1', 'Role_2']],
        30 => ['user' => 3, 'skill' => 2, 'roles' => ['Role_1']],
        40 => ['user' => 4, 'skill' => 2, 'roles' => ['Role_2']],
    ]);

    $result = $data->groupBy(['skill', function (array $item) {
        return $item['roles'];
    }], preserveKeys: true);

    /*
    [
        1 => [
            'Role_1' => [
                10 => ['user' => 1, 'skill' => 1, 'roles' => ['Role_1', 'Role_3']],
                20 => ['user' => 2, 'skill' => 1, 'roles' => ['Role_1', 'Role_2']],
            ],
            'Role_2' => [
                20 => ['user' => 2, 'skill' => 1, 'roles' => ['Role_1', 'Role_2']],
            ],
            'Role_3' => [
                10 => ['user' => 1, 'skill' => 1, 'roles' => ['Role_1', 'Role_3']],
            ],
        ],
        2 => [
            'Role_1' => [
                30 => ['user' => 3, 'skill' => 2, 'roles' => ['Role_1']],
            ],
            'Role_2' => [
                40 => ['user' => 4, 'skill' => 2, 'roles' => ['Role_2']],
            ],
        ],
    ];
    */

<a name="method-has"></a>
#### `has()` {.collection-method}

`has` メソッドは、指定されたキーがコレクションに存在するかどうかを判断します。

    $collection = collect(['account_id' => 1, 'product' => 'Desk', 'amount' => 5]);

    $collection->has('product');

    // true

    $collection->has(['product', 'amount']);

    // true

    $collection->has(['amount', 'price']);

    // false

<a name="method-hasany"></a>
#### `hasAny()` {.collection-method}

`hasAny` メソッドは、指定されたキーのいずれかがコレクションに存在するかどうかを判断します。

    $collection = collect(['account_id' => 1, 'product' => 'Desk', 'amount' => 5]);

    $collection->hasAny(['product', 'price']);

    // true

    $collection->hasAny(['name', 'price']);

    // false

<a name="method-implode"></a>
#### `implode()` {.collection-method}

`implode` メソッドは、コレクション内の項目を結合します。その引数は、コレクション内の項目のタイプによって異なります。コレクションに配列またはオブジェクトが含まれている場合は、結合する属性のキーと、値の間に配置する「接着剤」文字列を渡す必要があります。

    $collection = collect([
        ['account_id' => 1, 'product' => 'Desk'],
        ['account_id' => 2, 'product' => 'Chair'],
    ]);

    $collection->implode('product', ', ');

    // Desk, Chair

コレクションに単純な文字列または数値が含まれている場合は、メソッドの唯一の引数として「接着剤」を渡す必要があります。

    collect([1, 2, 3, 4, 5])->implode('-');

    // '1-2-3-4-5'

内部分解される値をフォーマットしたい場合は、`implode` メソッドにクロージャーを渡すことができます。

    $collection->implode(function (array $item, int $key) {
        return strtoupper($item['product']);
    }, ', ');

    // DESK, CHAIR

<a name="method-intersect"></a>
#### `intersect()` {.collection-method}

`intersect` メソッドは、指定された `array` またはコレクションに存在しない値を元のコレクションから削除します。結果として得られるコレクションは、元のコレクションのキーを保持します。

    $collection = collect(['Desk', 'Sofa', 'Chair']);

    $intersect = $collection->intersect(['Desk', 'Chair', 'Bookcase']);

    $intersect->all();

    // [0 => 'Desk', 2 => 'Chair']

> [!NOTE]  
> [Eloquent コレクション](/docs/{{version}}/eloquent-collections#method-intersect) を使用すると、このメソッドの動作が変更されます。

<a name="method-intersectAssoc"></a>
#### `intersectAssoc()` {.collection-method}

`intersectAssoc` メソッドは、元のコレクションを別のコレクションまたは `array` と比較し、指定されたすべてのコレクションに存在するキーと値のペアを返します。

    $collection = collect([
        'color' => 'red',
        'size' => 'M',
        'material' => 'cotton'
    ]);

    $intersect = $collection->intersectAssoc([
        'color' => 'blue',
        'size' => 'M',
        'material' => 'polyester'
    ]);

    $intersect->all();

    // ['size' => 'M']

<a name="method-intersectbykeys"></a>
#### `intersectByKeys()` {.collection-method}

`intersectByKeys` メソッドは、指定された `array` またはコレクションに存在しないキーとそれに対応する値を元のコレクションから削除します。

    $collection = collect([
        'serial' => 'UX301', 'type' => 'screen', 'year' => 2009,
    ]);

    $intersect = $collection->intersectByKeys([
        'reference' => 'UX404', 'type' => 'tab', 'year' => 2011,
    ]);

    $intersect->all();

    // ['type' => 'screen', 'year' => 2009]

<a name="method-isempty"></a>
#### `isEmpty()` {.collection-method}

`isEmpty` メソッドは、コレクションが空の場合は `true` を返します。それ以外の場合は、`false` が返されます。

    collect([])->isEmpty();

    // true

<a name="method-isnotempty"></a>
#### `isNotEmpty()` {.collection-method}

コレクションが空でない場合、`isNotEmpty` メソッドは `true` を返します。それ以外の場合は、`false` が返されます。

    collect([])->isNotEmpty();

    // false

<a name="method-join"></a>
#### `join()` {.collection-method}

`join` メソッドは、コレクションの値を文字列と結合します。このメソッドの 2 番目の引数を使用して、最後の要素を文字列に追加する方法を指定することもできます。

    collect(['a', 'b', 'c'])->join(', '); // 'a, b, c'
    collect(['a', 'b', 'c'])->join(', ', ', and '); // 'a, b, and c'
    collect(['a', 'b'])->join(', ', ' and '); // 'a and b'
    collect(['a'])->join(', ', ' and '); // 'a'
    collect([])->join(', ', ' and '); // ''

<a name="method-keyby"></a>
#### `keyBy()` {.collection-method}

`keyBy` メソッドは、指定されたキーによってコレクションにキーを設定します。複数の項目が同じキーを持つ場合、最後の項目だけが新しいコレクションに表示されます。

    $collection = collect([
        ['product_id' => 'prod-100', 'name' => 'Desk'],
        ['product_id' => 'prod-200', 'name' => 'Chair'],
    ]);

    $keyed = $collection->keyBy('product_id');

    $keyed->all();

    /*
        [
            'prod-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],
            'prod-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],
        ]
    */

メソッドにコールバックを渡すこともできます。コールバックは、次のようにしてコレクションのキーとなる値を返す必要があります。

    $keyed = $collection->keyBy(function (array $item, int $key) {
        return strtoupper($item['product_id']);
    });

    $keyed->all();

    /*
        [
            'PROD-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],
            'PROD-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],
        ]
    */

<a name="method-keys"></a>
#### `keys()` {.collection-method}

`keys` メソッドは、コレクションのすべてのキーを返します。

    $collection = collect([
        'prod-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],
        'prod-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],
    ]);

    $keys = $collection->keys();

    $keys->all();

    // ['prod-100', 'prod-200']

<a name="method-last"></a>
#### `last()` {.collection-method}

`last` メソッドは、指定された真理テストに合格したコレクション内の最後の要素を返します。

    collect([1, 2, 3, 4])->last(function (int $value, int $key) {
        return $value < 3;
    });

    // 2

引数なしで `last` メソッドを呼び出して、コレクション内の最後の要素を取得することもできます。コレクションが空の場合、`null` が返されます。

    collect([1, 2, 3, 4])->last();

    // 4

<a name="method-lazy"></a>
#### `lazy()` {.collection-method}

`lazy` メソッドは、基になる項目の配列から新しい [`LazyCollection`](#lazy-collections) インスタンスを返します。

    $lazyCollection = collect([1, 2, 3, 4])->lazy();

    $lazyCollection::class;

    // Illuminate\Support\LazyCollection

    $lazyCollection->all();

    // [1, 2, 3, 4]

これは、多くの項目を含む巨大な `Collection` に対して変換を実行する必要がある場合に特に便利です。

    $count = $hugeCollection
        ->lazy()
        ->where('country', 'FR')
        ->where('balance', '>', '100')
        ->count();

コレクションを `LazyCollection` に変換することで、大量の追加メモリを割り当てる必要がなくなります。元のコレクションはメモリ内に _its_ 値を保持しますが、後続のフィルターは保持しません。したがって、コレクションの結果をフィルタリングするときに追加のメモリが割り当てられることは事実上ありません。

<a name="method-macro"></a>
#### `macro()` {.collection-method}

静的 `macro` メソッドを使用すると、実行時に `Collection` クラスにメソッドを追加できます。詳細については、[コレクションの拡張](#extending-collections) のドキュメントを参照してください。

<a name="method-make"></a>
#### `make()` {.collection-method}

静的 `make` メソッドは、新しいコレクション インスタンスを作成します。 「[コレクションの作成](#creating-collections)」セクションを参照してください。

<a name="method-map"></a>
#### `map()` {.collection-method}

`map` メソッドはコレクションを反復処理し、各値を指定されたコールバックに渡します。コールバックは自由に項目を変更して返し、変更された項目の新しいコレクションを形成します。

    $collection = collect([1, 2, 3, 4, 5]);

    $multiplied = $collection->map(function (int $item, int $key) {
        return $item * 2;
    });

    $multiplied->all();

    // [2, 4, 6, 8, 10]

> [!WARNING]  
> 他のほとんどのコレクション メソッドと同様に、`map` は新しいコレクション インスタンスを返します。呼び出されるコレクションは変更されません。元のコレクションを変換する場合は、[`transform`](#method-transform) メソッドを使用します。

<a name="method-mapinto"></a>
#### `mapInto()` {.collection-method}

`mapInto()` メソッドはコレクションを反復処理し、値をコンストラクターに渡すことによって、指定されたクラスの新しいインスタンスを作成します。

    class Currency
    {
        /**
         * Create a new currency instance.
         */
        function __construct(
            public string $code
        ) {}
    }

    $collection = collect(['USD', 'EUR', 'GBP']);

    $currencies = $collection->mapInto(Currency::class);

    $currencies->all();

    // [Currency('USD'), Currency('EUR'), Currency('GBP')]

<a name="method-mapspread"></a>
#### `mapSpread()` {.collection-method}

`mapSpread` メソッドはコレクションの項目を反復処理し、ネストされた各項目の値を指定されたクロージャに渡します。クロージャは自由に項目を変更して返すことができるため、変更された項目の新しいコレクションが形成されます。

    $collection = collect([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);

    $chunks = $collection->chunk(2);

    $sequence = $chunks->mapSpread(function (int $even, int $odd) {
        return $even + $odd;
    });

    $sequence->all();

    // [1, 5, 9, 13, 17]

<a name="method-maptogroups"></a>
#### `mapToGroups()` {.collection-method}

`mapToGroups` メソッドは、指定されたクロージャによってコレクションの項目をグループ化します。クロージャは、単一のキーと値のペアを含む連想配列を返し、グループ化された値の新しいコレクションを形成する必要があります。

    $collection = collect([
        [
            'name' => 'John Doe',
            'department' => 'Sales',
        ],
        [
            'name' => 'Jane Doe',
            'department' => 'Sales',
        ],
        [
            'name' => 'Johnny Doe',
            'department' => 'Marketing',
        ]
    ]);

    $grouped = $collection->mapToGroups(function (array $item, int $key) {
        return [$item['department'] => $item['name']];
    });

    $grouped->all();

    /*
        [
            'Sales' => ['John Doe', 'Jane Doe'],
            'Marketing' => ['Johnny Doe'],
        ]
    */

    $grouped->get('Sales')->all();

    // ['John Doe', 'Jane Doe']

<a name="method-mapwithkeys"></a>
#### `mapWithKeys()` {.collection-method}

`mapWithKeys` メソッドはコレクションを反復処理し、各値を指定されたコールバックに渡します。コールバックは、単一のキーと値のペアを含む連想配列を返す必要があります。

    $collection = collect([
        [
            'name' => 'John',
            'department' => 'Sales',
            'email' => 'john@example.com',
        ],
        [
            'name' => 'Jane',
            'department' => 'Marketing',
            'email' => 'jane@example.com',
        ]
    ]);

    $keyed = $collection->mapWithKeys(function (array $item, int $key) {
        return [$item['email'] => $item['name']];
    });

    $keyed->all();

    /*
        [
            'john@example.com' => 'John',
            'jane@example.com' => 'Jane',
        ]
    */

<a name="method-max"></a>
#### `max()` {.collection-method}

`max` メソッドは、指定されたキーの最大値を返します。

    $max = collect([
        ['foo' => 10],
        ['foo' => 20]
    ])->max('foo');

    // 20

    $max = collect([1, 2, 3, 4, 5])->max();

    // 5

<a name="method-median"></a>
#### `median()` {.collection-method}

`median` メソッドは、指定されたキーの [中央値](https://en.wikipedia.org/wiki/Median) を返します。

    $median = collect([
        ['foo' => 10],
        ['foo' => 10],
        ['foo' => 20],
        ['foo' => 40]
    ])->median('foo');

    // 15

    $median = collect([1, 1, 2, 4])->median();

    // 1.5

<a name="method-merge"></a>
#### `merge()` {.collection-method}

`merge` メソッドは、指定された配列またはコレクションを元のコレクションとマージします。指定された項目の文字列キーが元のコレクションの文字列キーと一致する場合、指定された項目の値は元のコレクションの値を上書きします。

    $collection = collect(['product_id' => 1, 'price' => 100]);

    $merged = $collection->merge(['price' => 200, 'discount' => false]);

    $merged->all();

    // ['product_id' => 1, 'price' => 200, 'discount' => false]

指定された項目のキーが数値の場合、値はコレクションの末尾に追加されます。

    $collection = collect(['Desk', 'Chair']);

    $merged = $collection->merge(['Bookcase', 'Door']);

    $merged->all();

    // ['Desk', 'Chair', 'Bookcase', 'Door']

<a name="method-mergerecursive"></a>
#### `mergeRecursive()` {.collection-method}

`mergeRecursive` メソッドは、指定された配列またはコレクションを元のコレクションと再帰的にマージします。指定された項目の文字列キーが元のコレクションの文字列キーと一致する場合、これらのキーの値が配列にマージされ、これが再帰的に行われます。

    $collection = collect(['product_id' => 1, 'price' => 100]);

    $merged = $collection->mergeRecursive([
        'product_id' => 2,
        'price' => 200,
        'discount' => false
    ]);

    $merged->all();

    // ['product_id' => [1, 2], 'price' => [100, 200], 'discount' => false]

<a name="method-min"></a>
#### `min()` {.collection-method}

`min` メソッドは、指定されたキーの最小値を返します。

    $min = collect([['foo' => 10], ['foo' => 20]])->min('foo');

    // 10

    $min = collect([1, 2, 3, 4, 5])->min();

    // 1

<a name="method-mode"></a>
#### `mode()` {.collection-method}

`mode` メソッドは、指定されたキーの [モード値](https://en.wikipedia.org/wiki/Mode_(statistics)) を返します。

    $mode = collect([
        ['foo' => 10],
        ['foo' => 10],
        ['foo' => 20],
        ['foo' => 40]
    ])->mode('foo');

    // [10]

    $mode = collect([1, 1, 2, 4])->mode();

    // [1]

    $mode = collect([1, 1, 2, 2])->mode();

    // [1, 2]

<a name="method-nth"></a>
#### `nth()` {.collection-method}

`nth` メソッドは、n 番目ごとの要素で構成される新しいコレクションを作成します。

    $collection = collect(['a', 'b', 'c', 'd', 'e', 'f']);

    $collection->nth(4);

    // ['a', 'e']

オプションで、開始オフセットを 2 番目の引数として渡すこともできます。

    $collection->nth(4, 1);

    // ['b', 'f']

<a name="method-only"></a>
#### `only()` {.collection-method}

`only` メソッドは、指定されたキーを持つコレクション内の項目を返します。

    $collection = collect([
        'product_id' => 1,
        'name' => 'Desk',
        'price' => 100,
        'discount' => false
    ]);

    $filtered = $collection->only(['product_id', 'name']);

    $filtered->all();

    // ['product_id' => 1, 'name' => 'Desk']

`only` の逆については、[except](#method-except) メソッドを参照してください。

> [!NOTE]  
> [Eloquent コレクション](/docs/{{version}}/eloquent-collections#method-only) を使用すると、このメソッドの動作が変更されます。

<a name="method-pad"></a>
#### `pad()` {.collection-method}

`pad` メソッドは、配列が指定されたサイズに達するまで、指定された値で配列を埋めます。このメソッドは、[array_pad](https://secure.php.net/manual/en/function.array-pad.php) PHP 関数と同様に動作します。

左側をパディングするには、負のサイズを指定する必要があります。指定されたサイズの絶対値が配列の長さ以下の場合、パディングは行われません。

    $collection = collect(['A', 'B', 'C']);

    $filtered = $collection->pad(5, 0);

    $filtered->all();

    // ['A', 'B', 'C', 0, 0]

    $filtered = $collection->pad(-5, 0);

    $filtered->all();

    // [0, 0, 'A', 'B', 'C']

<a name="method-partition"></a>
#### `partition()` {.collection-method}

`partition` メソッドを PHP 配列の構造化と組み合わせて、特定の真実テストに合格する要素とそうでない要素を分離することができます。

    $collection = collect([1, 2, 3, 4, 5, 6]);

    [$underThree, $equalOrAboveThree] = $collection->partition(function (int $i) {
        return $i < 3;
    });

    $underThree->all();

    // [1, 2]

    $equalOrAboveThree->all();

    // [3, 4, 5, 6]

<a name="method-percentage"></a>
#### `percentage()` {.collection-method}

`percentage` メソッドを使用すると、コレクション内の特定の真実テストに合格したアイテムの割合を迅速に判断できます。

```php
$collection = collect([1, 1, 2, 2, 2, 3]);

$percentage = $collection->percentage(fn ($value) => $value === 1);

// 33.33
```

デフォルトでは、パーセンテージは小数点第 2 位に四捨五入されます。ただし、メソッドに 2 番目の引数を指定することで、この動作をカスタマイズできます。

```php
$percentage = $collection->percentage(fn ($value) => $value === 1, precision: 3);

// 33.333
```

<a name="method-pipe"></a>
#### `pipe()` {.collection-method}

`pipe` メソッドは、コレクションを指定されたクロージャに渡し、実行されたクロージャの結果を返します。

    $collection = collect([1, 2, 3]);

    $piped = $collection->pipe(function (Collection $collection) {
        return $collection->sum();
    });

    // 6

<a name="method-pipeinto"></a>
#### `pipeInto()` {.collection-method}

`pipeInto` メソッドは、指定されたクラスの新しいインスタンスを作成し、コレクションをコンストラクターに渡します。

    class ResourceCollection
    {
        /**
         * Create a new ResourceCollection instance.
         */
        public function __construct(
          public Collection $collection,
        ) {}
    }

    $collection = collect([1, 2, 3]);

    $resource = $collection->pipeInto(ResourceCollection::class);

    $resource->collection->all();

    // [1, 2, 3]

<a name="method-pipethrough"></a>
#### `pipeThrough()` {.collection-method}

`pipeThrough` メソッドは、コレクションを指定されたクロージャの配列に渡し、実行されたクロージャの結果を返します。

    use Illuminate\Support\Collection;

    $collection = collect([1, 2, 3]);

    $result = $collection->pipeThrough([
        function (Collection $collection) {
            return $collection->merge([4, 5]);
        },
        function (Collection $collection) {
            return $collection->sum();
        },
    ]);

    // 15

<a name="method-pluck"></a>
#### `pluck()` {.collection-method}

`pluck` メソッドは、指定されたキーのすべての値を取得します。

    $collection = collect([
        ['product_id' => 'prod-100', 'name' => 'Desk'],
        ['product_id' => 'prod-200', 'name' => 'Chair'],
    ]);

    $plucked = $collection->pluck('name');

    $plucked->all();

    // ['Desk', 'Chair']

結果のコレクションにどのようにキーを設定するかを指定することもできます。

    $plucked = $collection->pluck('name', 'product_id');

    $plucked->all();

    // ['prod-100' => 'Desk', 'prod-200' => 'Chair']

`pluck` メソッドは、「ドット」表記を使用したネストされた値の取得もサポートしています。

    $collection = collect([
        [
            'name' => 'Laracon',
            'speakers' => [
                'first_day' => ['Rosa', 'Judith'],
            ],
        ],
        [
            'name' => 'VueConf',
            'speakers' => [
                'first_day' => ['Abigail', 'Joey'],
            ],
        ],
    ]);

    $plucked = $collection->pluck('speakers.first_day');

    $plucked->all();

    // [['Rosa', 'Judith'], ['Abigail', 'Joey']]

重複したキーが存在する場合、最後に一致した要素が取り出されたコレクションに挿入されます。

    $collection = collect([
        ['brand' => 'Tesla',  'color' => 'red'],
        ['brand' => 'Pagani', 'color' => 'white'],
        ['brand' => 'Tesla',  'color' => 'black'],
        ['brand' => 'Pagani', 'color' => 'orange'],
    ]);

    $plucked = $collection->pluck('color', 'brand');

    $plucked->all();

    // ['Tesla' => 'black', 'Pagani' => 'orange']

<a name="method-pop"></a>
#### `pop()` {.collection-method}

`pop` メソッドは、コレクションから最後の項目を削除して返します。

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->pop();

    // 5

    $collection->all();

    // [1, 2, 3, 4]

整数を `pop` メソッドに渡して、コレクションの末尾から複数の項目を削除して返すことができます。

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->pop(3);

    // collect([5, 4, 3])

    $collection->all();

    // [1, 2]

<a name="method-prepend"></a>
#### `prepend()` {.collection-method}

`prepend` メソッドは、コレクションの先頭に項目を追加します。

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->prepend(0);

    $collection->all();

    // [0, 1, 2, 3, 4, 5]

2 番目の引数を渡して、先頭に追加される項目のキーを指定することもできます。

    $collection = collect(['one' => 1, 'two' => 2]);

    $collection->prepend(0, 'zero');

    $collection->all();

    // ['zero' => 0, 'one' => 1, 'two' => 2]

<a name="method-pull"></a>
#### `pull()` {.collection-method}

`pull` メソッドは、キーによってコレクションから項目を削除して返します。

    $collection = collect(['product_id' => 'prod-100', 'name' => 'Desk']);

    $collection->pull('name');

    // 'Desk'

    $collection->all();

    // ['product_id' => 'prod-100']

<a name="method-push"></a>
#### `push()` {.collection-method}

`push` メソッドは、コレクションの末尾に項目を追加します。

    $collection = collect([1, 2, 3, 4]);

    $collection->push(5);

    $collection->all();

    // [1, 2, 3, 4, 5]

<a name="method-put"></a>
#### `put()` {.collection-method}

`put` メソッドは、コレクション内の指定されたキーと値を設定します。

    $collection = collect(['product_id' => 1, 'name' => 'Desk']);

    $collection->put('price', 100);

    $collection->all();

    // ['product_id' => 1, 'name' => 'Desk', 'price' => 100]

<a name="method-random"></a>
#### `random()` {.collection-method}

`random` メソッドは、コレクションからランダムな項目を返します。

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->random();

    // 4 - (retrieved randomly)

整数を `random` に渡して、ランダムに取得する項目の数を指定できます。受け取りたい項目の数を明示的に渡すと、常に項目のコレクションが返されます。

    $random = $collection->random(3);

    $random->all();

    // [2, 4, 5] - (retrieved randomly)

コレクション インスタンスのアイテムが要求されたアイテムよりも少ない場合、`random` メソッドは `InvalidArgumentException` をスローします。

`random` メソッドは、現在のコレクション インスタンスを受け取るクロージャも受け入れます。

    use Illuminate\Support\Collection;

    $random = $collection->random(fn (Collection $items) => min(10, count($items)));

    $random->all();

    // [1, 2, 3, 4, 5] - (retrieved randomly)

<a name="method-range"></a>
#### `range()` {.collection-method}

`range` メソッドは、指定された範囲内の整数を含むコレクションを返します。

    $collection = collect()->range(3, 6);

    $collection->all();

    // [3, 4, 5, 6]

<a name="method-reduce"></a>
#### `reduce()` {.collection-method}

`reduce` メソッドは、コレクションを単一の値に減らし、各反復の結果を後続の反復に渡します。

    $collection = collect([1, 2, 3]);

    $total = $collection->reduce(function (?int $carry, int $item) {
        return $carry + $item;
    });

    // 6

最初の反復の `$carry` の値は `null` です。ただし、2 番目の引数を `reduce` に渡すことで、その初期値を指定できます。

    $collection->reduce(function (int $carry, int $item) {
        return $carry + $item;
    }, 4);

    // 10

`reduce` メソッドは、連想コレクション内の配列キーも指定されたコールバックに渡します。

    $collection = collect([
        'usd' => 1400,
        'gbp' => 1200,
        'eur' => 1000,
    ]);

    $ratio = [
        'usd' => 1,
        'gbp' => 1.37,
        'eur' => 1.22,
    ];

    $collection->reduce(function (int $carry, int $value, int $key) use ($ratio) {
        return $carry + ($value * $ratio[$key]);
    });

    // 4264
    
<a name="method-reduce-spread"></a>
#### `reduceSpread()` {.collection-method}

`reduceSpread` メソッドは、コレクションを値の配列に縮小し、各反復の結果を後続の反復に渡します。このメソッドは、`reduce` メソッドに似ています。ただし、複数の初期値を受け入れることができます。

    [$creditsRemaining, $batch] = Image::where('status', 'unprocessed')
        ->get()
        ->reduceSpread(function (int $creditsRemaining, Collection $batch, Image $image) {
            if ($creditsRemaining >= $image->creditsRequired()) {
                $batch->push($image);

                $creditsRemaining -= $image->creditsRequired();
            }

            return [$creditsRemaining, $batch];
        }, $creditsAvailable, collect());

<a name="method-reject"></a>
#### `reject()` {.collection-method}

`reject` メソッドは、指定されたクロージャーを使用してコレクションをフィルターします。結果のコレクションから項目を削除する必要がある場合、クロージャは `true` を返す必要があります。

    $collection = collect([1, 2, 3, 4]);

    $filtered = $collection->reject(function (int $value, int $key) {
        return $value > 2;
    });

    $filtered->all();

    // [1, 2]

`reject` メソッドの逆については、[`filter`](#method-filter) メソッドを参照してください。

<a name="method-replace"></a>
#### `replace()` {.collection-method}

`replace` メソッドは、`merge` と同様に動作します。ただし、`replace` メソッドは、文字列キーを持つ一致する項目を上書きするだけでなく、一致する数値キーを持つコレクション内の項目も上書きします。

    $collection = collect(['Taylor', 'Abigail', 'James']);

    $replaced = $collection->replace([1 => 'Victoria', 3 => 'Finn']);

    $replaced->all();

    // ['Taylor', 'Victoria', 'James', 'Finn']

<a name="method-replacerecursive"></a>
#### `replaceRecursive()` {.collection-method}

このメソッドは `replace` と同様に機能しますが、配列内で再帰的に実行され、同じ置換プロセスが内部値に適用されます。

    $collection = collect([
        'Taylor',
        'Abigail',
        [
            'James',
            'Victoria',
            'Finn'
        ]
    ]);

    $replaced = $collection->replaceRecursive([
        'Charlie',
        2 => [1 => 'King']
    ]);

    $replaced->all();

    // ['Charlie', 'Abigail', ['James', 'King', 'Finn']]

<a name="method-reverse"></a>
#### `reverse()` {.collection-method}

`reverse` メソッドは、元のキーを保持したまま、コレクションの項目の順序を逆にします。

    $collection = collect(['a', 'b', 'c', 'd', 'e']);

    $reversed = $collection->reverse();

    $reversed->all();

    /*
        [
            4 => 'e',
            3 => 'd',
            2 => 'c',
            1 => 'b',
            0 => 'a',
        ]
    */

<a name="method-search"></a>
#### `search()` {.collection-method}

`search` メソッドは、コレクション内で指定された値を検索し、見つかった場合はそのキーを返します。項目が見つからない場合は、`false` が返されます。

    $collection = collect([2, 4, 6, 8]);

    $collection->search(4);

    // 1

検索は「緩やかな」比較を使用して行われます。つまり、整数値を持つ文字列は同じ値の整数と等しいと見なされます。 「厳密な」比較を使用するには、メソッドの 2 番目の引数として `true` を渡します。

    collect([2, 4, 6, 8])->search('4', $strict = true);

    // false

あるいは、独自のクロージャを提供して、指定された真理テストに合格する最初の項目を検索することもできます。

    collect([2, 4, 6, 8])->search(function (int $item, int $key) {
        return $item > 5;
    });

    // 2

<a name="method-select"></a>
#### `select()` {.collection-method}

`select` メソッドは、SQL `SELECT` ステートメントと同様に、コレクションから指定されたキーを選択します。

```php
$users = collect([
    ['name' => 'Taylor Otwell', 'role' => 'Developer', 'status' => 'active'],
    ['name' => 'Victoria Faith', 'role' => 'Researcher', 'status' => 'active'],
]);

$users->select(['name', 'role']);

/*
    [
        ['name' => 'Taylor Otwell', 'role' => 'Developer'],
        ['name' => 'Victoria Faith', 'role' => 'Researcher'],
    ],
*/
```

<a name="method-shift"></a>
#### `shift()` {.collection-method}

`shift` メソッドは、コレクションから最初の項目を削除して返します。

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->shift();

    // 1

    $collection->all();

    // [2, 3, 4, 5]

整数を `shift` メソッドに渡して、コレクションの先頭から複数の項目を削除して返すことができます。

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->shift(3);

    // collect([1, 2, 3])

    $collection->all();

    // [4, 5]

<a name="method-shuffle"></a>
#### `shuffle()` {.collection-method}

`shuffle` メソッドは、コレクション内の項目をランダムにシャッフルします。

    $collection = collect([1, 2, 3, 4, 5]);

    $shuffled = $collection->shuffle();

    $shuffled->all();

    // [3, 2, 5, 1, 4] - (generated randomly)

<a name="method-skip"></a>
#### `skip()` {.collection-method}

`skip` メソッドは、コレクションの先頭から指定された数の要素が削除された新しいコレクションを返します。

    $collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

    $collection = $collection->skip(4);

    $collection->all();

    // [5, 6, 7, 8, 9, 10]

<a name="method-skipuntil"></a>
#### `skipUntil()` {.collection-method}

`skipUntil` メソッドは、指定されたコールバックが `true` を返すまでコレクションの項目をスキップし、その後コレクション内の残りの項目を新しいコレクション インスタンスとして返します。

    $collection = collect([1, 2, 3, 4]);

    $subset = $collection->skipUntil(function (int $item) {
        return $item >= 3;
    });

    $subset->all();

    // [3, 4]

単純な値を `skipUntil` メソッドに渡して、指定された値が見つかるまですべての項目をスキップすることもできます。

    $collection = collect([1, 2, 3, 4]);

    $subset = $collection->skipUntil(3);

    $subset->all();

    // [3, 4]

> [!WARNING]  
> 指定された値が見つからない場合、またはコールバックが `true` を返さない場合、`skipUntil` メソッドは空のコレクションを返します。

<a name="method-skipwhile"></a>
#### `skipWhile()` {.collection-method}

`skipWhile` メソッドはコレクションの項目をスキップし、指定されたコールバックは `true` を返し、コレクション内の残りの項目を新しいコレクションとして返します。

    $collection = collect([1, 2, 3, 4]);

    $subset = $collection->skipWhile(function (int $item) {
        return $item <= 3;
    });

    $subset->all();

    // [4]

> [!WARNING]  
> コールバックが `false` を返さない場合、`skipWhile` メソッドは空のコレクションを返します。

<a name="method-slice"></a>
#### `slice()` {.collection-method}

`slice` メソッドは、指定されたインデックスから始まるコレクションのスライスを返します。

    $collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

    $slice = $collection->slice(4);

    $slice->all();

    // [5, 6, 7, 8, 9, 10]

返されるスライスのサイズを制限したい場合は、目的のサイズを 2 番目の引数としてメソッドに渡します。

    $slice = $collection->slice(4, 2);

    $slice->all();

    // [5, 6]

返されたスライスはデフォルトでキーを保持します。元のキーを保持したくない場合は、[`values`](#method-values) メソッドを使用してインデックスを再作成できます。

<a name="method-sliding"></a>
#### `sliding()` {.collection-method}

`sliding` メソッドは、コレクション内の項目の「スライディング ウィンドウ」ビューを表すチャンクの新しいコレクションを返します。

    $collection = collect([1, 2, 3, 4, 5]);

    $chunks = $collection->sliding(2);

    $chunks->toArray();

    // [[1, 2], [2, 3], [3, 4], [4, 5]]

これは、[`eachSpread`](#method-eachspread) メソッドと組み合わせると特に便利です。

    $transactions->sliding(2)->eachSpread(function (Collection $previous, Collection $current) {
        $current->total = $previous->total + $current->amount;
    });

オプションで、各チャンクの最初の項目間の距離を決定する 2 番目の「ステップ」値を渡すこともできます。

    $collection = collect([1, 2, 3, 4, 5]);

    $chunks = $collection->sliding(3, step: 2);

    $chunks->toArray();

    // [[1, 2, 3], [3, 4, 5]]

<a name="method-sole"></a>
#### `sole()` {.collection-method}

`sole` メソッドは、指定された真実テストに合格したコレクション内の最初の要素を返します。ただし、真実テストが 1 つの要素と正確に一致する場合に限ります。

    collect([1, 2, 3, 4])->sole(function (int $value, int $key) {
        return $value === 2;
    });

    // 2

キーと値のペアを `sole` メソッドに渡すこともできます。これは、指定されたペアに一致するコレクション内の最初の要素を返しますが、それは 1 つの要素が正確に一致する場合に限られます。

    $collection = collect([
        ['product' => 'Desk', 'price' => 200],
        ['product' => 'Chair', 'price' => 100],
    ]);

    $collection->sole('product', 'Chair');

    // ['product' => 'Chair', 'price' => 100]

あるいは、要素が 1 つしかない場合は、引数なしで `sole` メソッドを呼び出して、コレクション内の最初の要素を取得することもできます。

    $collection = collect([
        ['product' => 'Desk', 'price' => 200],
    ]);

    $collection->sole();

    // ['product' => 'Desk', 'price' => 200]

`sole` メソッドによって返される必要がある要素がコレクション内にない場合、`\Illuminate\Collections\ItemNotFoundException` 例外がスローされます。返すべき要素が複数ある場合は、`\Illuminate\Collections\MultipleItemsFoundException` がスローされます。

<a name="method-some"></a>
#### `some()` {.collection-method}

[`contains`](#method-contains) メソッドのエイリアス。

<a name="method-sort"></a>
#### `sort()` {.collection-method}

`sort` メソッドはコレクションを並べ替えます。並べ替えられたコレクションには元の配列キーが保持されるため、次の例では、[`values`](#method-values) メソッドを使用してキーを連続番号のインデックスにリセットします。

    $collection = collect([5, 3, 1, 2, 4]);

    $sorted = $collection->sort();

    $sorted->values()->all();

    // [1, 2, 3, 4, 5]

並べ替えのニーズがさらに高度な場合は、独自のアルゴリズムを使用して `sort` にコールバックを渡すことができます。 [`uasort`](https://secure.php.net/manual/en/function.uasort.php#refsect1-function.uasort-parameters) に関する PHP ドキュメントを参照してください。これは、コレクションの `sort` メソッド呼び出しが内部的に利用するものです。

> [!NOTE]  
> ネストされた配列またはオブジェクトのコレクションを並べ替える必要がある場合は、[`sortBy`](#method-sortby) メソッドと [`sortByDesc`](#method-sortbydesc) メソッドを参照してください。

<a name="method-sortby"></a>
#### `sortBy()` {.collection-method}

`sortBy` メソッドは、指定されたキーでコレクションを並べ替えます。並べ替えられたコレクションには元の配列キーが保持されるため、次の例では、[`values`](#method-values) メソッドを使用してキーを連続番号のインデックスにリセットします。

    $collection = collect([
        ['name' => 'Desk', 'price' => 200],
        ['name' => 'Chair', 'price' => 100],
        ['name' => 'Bookcase', 'price' => 150],
    ]);

    $sorted = $collection->sortBy('price');

    $sorted->values()->all();

    /*
        [
            ['name' => 'Chair', 'price' => 100],
            ['name' => 'Bookcase', 'price' => 150],
            ['name' => 'Desk', 'price' => 200],
        ]
    */

`sortBy` メソッドは、2 番目の引数として [ソートフラグ](https://www.php.net/manual/en/function.sort.php) を受け入れます。

    $collection = collect([
        ['title' => 'Item 1'],
        ['title' => 'Item 12'],
        ['title' => 'Item 3'],
    ]);

    $sorted = $collection->sortBy('title', SORT_NATURAL);

    $sorted->values()->all();

    /*
        [
            ['title' => 'Item 1'],
            ['title' => 'Item 3'],
            ['title' => 'Item 12'],
        ]
    */

あるいは、独自のクロージャを渡して、コレクションの値を並べ替える方法を決定することもできます。

    $collection = collect([
        ['name' => 'Desk', 'colors' => ['Black', 'Mahogany']],
        ['name' => 'Chair', 'colors' => ['Black']],
        ['name' => 'Bookcase', 'colors' => ['Red', 'Beige', 'Brown']],
    ]);

    $sorted = $collection->sortBy(function (array $product, int $key) {
        return count($product['colors']);
    });

    $sorted->values()->all();

    /*
        [
            ['name' => 'Chair', 'colors' => ['Black']],
            ['name' => 'Desk', 'colors' => ['Black', 'Mahogany']],
            ['name' => 'Bookcase', 'colors' => ['Red', 'Beige', 'Brown']],
        ]
    */

コレクションを複数の属性で並べ替えたい場合は、並べ替えの基準にする属性の配列を渡すことができます。

    $collection = collect([
        ['name' => 'Taylor Otwell', 'age' => 34],
        ['name' => 'Abigail Otwell', 'age' => 30],
        ['name' => 'Taylor Otwell', 'age' => 36],
        ['name' => 'Abigail Otwell', 'age' => 32],
    ]);

    $sorted = $collection->sortBy(['name', 'age']);

    $sorted->values()->all();

    /*
        [
            ['name' => 'Abigail Otwell', 'age' => 30],
            ['name' => 'Abigail Otwell', 'age' => 32],
            ['name' => 'Taylor Otwell', 'age' => 34],
            ['name' => 'Taylor Otwell', 'age' => 36],
        ]
    */



複数の属性および方向で並べ替える場合、並べ替え操作の配列を `sortBy` メソッドに渡すことができます。各ソート操作は、ソートの基準となる属性と目的のソートの方向で構成される配列である必要があります。

    $collection = collect([
        ['name' => 'Taylor Otwell', 'age' => 34],
        ['name' => 'Abigail Otwell', 'age' => 30],
        ['name' => 'Taylor Otwell', 'age' => 36],
        ['name' => 'Abigail Otwell', 'age' => 32],
    ]);

    $sorted = $collection->sortBy([
        ['name', 'asc'],
        ['age', 'desc'],
    ]);

    $sorted->values()->all();

    /*
        [
            ['name' => 'Abigail Otwell', 'age' => 32],
            ['name' => 'Abigail Otwell', 'age' => 30],
            ['name' => 'Taylor Otwell', 'age' => 36],
            ['name' => 'Taylor Otwell', 'age' => 34],
        ]
    */

複数の属性でコレクションを並べ替える場合、各並べ替え操作を定義するクロージャを提供することもできます。

    $collection = collect([
        ['name' => 'Taylor Otwell', 'age' => 34],
        ['name' => 'Abigail Otwell', 'age' => 30],
        ['name' => 'Taylor Otwell', 'age' => 36],
        ['name' => 'Abigail Otwell', 'age' => 32],
    ]);

    $sorted = $collection->sortBy([
        fn (array $a, array $b) => $a['name'] <=> $b['name'],
        fn (array $a, array $b) => $b['age'] <=> $a['age'],
    ]);

    $sorted->values()->all();

    /*
        [
            ['name' => 'Abigail Otwell', 'age' => 32],
            ['name' => 'Abigail Otwell', 'age' => 30],
            ['name' => 'Taylor Otwell', 'age' => 36],
            ['name' => 'Taylor Otwell', 'age' => 34],
        ]
    */

<a name="method-sortbydesc"></a>
#### `sortByDesc()` {.collection-method}

このメソッドは、[`sortBy`](#method-sortby) メソッドと同じシグネチャを持ちますが、コレクションを逆の順序で並べ替えます。

<a name="method-sortdesc"></a>
#### `sortDesc()` {.collection-method}

このメソッドは、[`sort`](#method-sort) メソッドとは逆の順序でコレクションを並べ替えます。

    $collection = collect([5, 3, 1, 2, 4]);

    $sorted = $collection->sortDesc();

    $sorted->values()->all();

    // [5, 4, 3, 2, 1]

`sort` とは異なり、クロージャを `sortDesc` に渡すことはできません。代わりに、[`sort`](#method-sort) メソッドを使用して、比較を反転する必要があります。

<a name="method-sortkeys"></a>
#### `sortKeys()` {.collection-method}

`sortKeys` メソッドは、基になる連想配列のキーによってコレクションを並べ替えます。

    $collection = collect([
        'id' => 22345,
        'first' => 'John',
        'last' => 'Doe',
    ]);

    $sorted = $collection->sortKeys();

    $sorted->all();

    /*
        [
            'first' => 'John',
            'id' => 22345,
            'last' => 'Doe',
        ]
    */

<a name="method-sortkeysdesc"></a>
#### `sortKeysDesc()` {.collection-method}

このメソッドは、[`sortKeys`](#method-sortkeys) メソッドと同じシグネチャを持ちますが、コレクションを逆の順序で並べ替えます。

<a name="method-sortkeysusing"></a>
#### `sortKeysUsing()` {.collection-method}

`sortKeysUsing` メソッドは、コールバックを使用して、基になる連想配列のキーによってコレクションを並べ替えます。

    $collection = collect([
        'ID' => 22345,
        'first' => 'John',
        'last' => 'Doe',
    ]);

    $sorted = $collection->sortKeysUsing('strnatcasecmp');

    $sorted->all();

    /*
        [
            'first' => 'John',
            'ID' => 22345,
            'last' => 'Doe',
        ]
    */

コールバックは、ゼロ以下、ゼロ以上の整数を返す比較関数である必要があります。詳細については、`sortKeysUsing` メソッドが内部で使用する PHP 関数である [`uksort`](https://www.php.net/manual/en/function.uksort.php#refsect1-function.uksort-parameters) に関する PHP ドキュメントを参照してください。

<a name="method-splice"></a>
#### `splice()` {.collection-method}

`splice` メソッドは、指定されたインデックスから始まる項目のスライスを削除して返します。

    $collection = collect([1, 2, 3, 4, 5]);

    $chunk = $collection->splice(2);

    $chunk->all();

    // [3, 4, 5]

    $collection->all();

    // [1, 2]

2 番目の引数を渡して、結果として得られるコレクションのサイズを制限できます。

    $collection = collect([1, 2, 3, 4, 5]);

    $chunk = $collection->splice(2, 1);

    $chunk->all();

    // [3]

    $collection->all();

    // [1, 2, 4, 5]

さらに、コレクションから削除された項目を置き換える新しい項目を含む 3 番目の引数を渡すこともできます。

    $collection = collect([1, 2, 3, 4, 5]);

    $chunk = $collection->splice(2, 1, [10, 11]);

    $chunk->all();

    // [3]

    $collection->all();

    // [1, 2, 10, 11, 4, 5]

<a name="method-split"></a>
#### `split()` {.collection-method}

`split` メソッドは、コレクションを指定された数のグループに分割します。

    $collection = collect([1, 2, 3, 4, 5]);

    $groups = $collection->split(3);

    $groups->all();

    // [[1, 2], [3, 4], [5]]

<a name="method-splitin"></a>
#### `splitIn()` {.collection-method}

`splitIn` メソッドは、コレクションを指定された数のグループに分割し、非終端グループを完全に埋めてから、残りを最後のグループに割り当てます。

    $collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

    $groups = $collection->splitIn(3);

    $groups->all();

    // [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10]]

<a name="method-sum"></a>
#### `sum()` {.collection-method}

`sum` メソッドは、コレクション内のすべての項目の合計を返します。

    collect([1, 2, 3, 4, 5])->sum();

    // 15

コレクションにネストされた配列またはオブジェクトが含まれている場合は、合計する値を決定するために使用されるキーを渡す必要があります。

    $collection = collect([
        ['name' => 'JavaScript: The Good Parts', 'pages' => 176],
        ['name' => 'JavaScript: The Definitive Guide', 'pages' => 1096],
    ]);

    $collection->sum('pages');

    // 1272

さらに、独自のクロージャを渡して、コレクションのどの値を合計するかを決定することもできます。

    $collection = collect([
        ['name' => 'Chair', 'colors' => ['Black']],
        ['name' => 'Desk', 'colors' => ['Black', 'Mahogany']],
        ['name' => 'Bookcase', 'colors' => ['Red', 'Beige', 'Brown']],
    ]);

    $collection->sum(function (array $product) {
        return count($product['colors']);
    });

    // 6

<a name="method-take"></a>
#### `take()` {.collection-method}

`take` メソッドは、指定された数の項目を含む新しいコレクションを返します。

    $collection = collect([0, 1, 2, 3, 4, 5]);

    $chunk = $collection->take(3);

    $chunk->all();

    // [0, 1, 2]

負の整数を渡して、コレクションの最後から指定した数の項目を取得することもできます。

    $collection = collect([0, 1, 2, 3, 4, 5]);

    $chunk = $collection->take(-2);

    $chunk->all();

    // [4, 5]

<a name="method-takeuntil"></a>
#### `takeUntil()` {.collection-method}

`takeUntil` メソッドは、指定されたコールバックが `true` を返すまで、コレクション内の項目を返します。

    $collection = collect([1, 2, 3, 4]);

    $subset = $collection->takeUntil(function (int $item) {
        return $item >= 3;
    });

    $subset->all();

    // [1, 2]

単純な値を `takeUntil` メソッドに渡して、指定された値が見つかるまで項目を取得することもできます。

    $collection = collect([1, 2, 3, 4]);

    $subset = $collection->takeUntil(3);

    $subset->all();

    // [1, 2]

> [!WARNING]  
> 指定された値が見つからない場合、またはコールバックが `true` を返さない場合、`takeUntil` メソッドはコレクション内のすべての項目を返します。

<a name="method-takewhile"></a>
#### `takeWhile()` {.collection-method}

`takeWhile` メソッドは、指定されたコールバックが `false` を返すまで、コレクション内の項目を返します。

    $collection = collect([1, 2, 3, 4]);

    $subset = $collection->takeWhile(function (int $item) {
        return $item < 3;
    });

    $subset->all();

    // [1, 2]

> [!WARNING]  
> コールバックが `false` を返さない場合、`takeWhile` メソッドはコレクション内のすべての項目を返します。

<a name="method-tap"></a>
#### `tap()` {.collection-method}

`tap` メソッドは、コレクションを指定されたコールバックに渡します。これにより、コレクション自体には影響を与えずに、特定の時点でコレクションに「タップ」し、項目に対して何らかの処理を行うことができます。その後、コレクションは `tap` メソッドによって返されます。

    collect([2, 4, 3, 1, 5])
        ->sort()
        ->tap(function (Collection $collection) {
            Log::debug('Values after sorting', $collection->values()->all());
        })
        ->shift();

    // 1

<a name="method-times"></a>
#### `times()` {.collection-method}

静的 `times` メソッドは、指定されたクロージャを指定された回数呼び出すことによって新しいコレクションを作成します。

    $collection = Collection::times(10, function (int $number) {
        return $number * 9;
    });

    $collection->all();

    // [9, 18, 27, 36, 45, 54, 63, 72, 81, 90]

<a name="method-toarray"></a>
#### `toArray()` {.collection-method}

`toArray` メソッドは、コレクションをプレーンな PHP `array` に変換します。コレクションの値が [Eloquent](/docs/{{version}}/eloquent) モデルの場合、モデルも配列に変換されます。

    $collection = collect(['name' => 'Desk', 'price' => 200]);

    $collection->toArray();

    /*
        [
            ['name' => 'Desk', 'price' => 200],
        ]
    */

> [!WARNING]  
> `toArray` は、`Arrayable` のインスタンスであるコレクションのネストされたオブジェクトもすべて配列に変換します。コレクションの基礎となる生の配列を取得したい場合は、代わりに [`all`](#method-all) メソッドを使用してください。

<a name="method-tojson"></a>
#### `toJson()` {.collection-method}

`toJson` メソッドは、コレクションを JSON シリアル化文字列に変換します。

    $collection = collect(['name' => 'Desk', 'price' => 200]);

    $collection->toJson();

    // '{"name":"Desk", "price":200}'

<a name="method-transform"></a>
#### `transform()` {.collection-method}

`transform` メソッドはコレクションを反復処理し、コレクション内の各項目で指定されたコールバックを呼び出します。コレクション内の項目は、コールバックによって返された値に置き換えられます。

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->transform(function (int $item, int $key) {
        return $item * 2;
    });

    $collection->all();

    // [2, 4, 6, 8, 10]

> [!WARNING]  
> 他のほとんどのコレクション メソッドとは異なり、`transform` はコレクション自体を変更します。代わりに新しいコレクションを作成する場合は、[`map`](#method-map) メソッドを使用します。

<a name="method-undot"></a>
#### `undot()` {.collection-method}

`undot` メソッドは、「ドット」表記を使用する単一次元のコレクションを多次元のコレクションに拡張します。

    $person = collect([
        'name.first_name' => 'Marie',
        'name.last_name' => 'Valentine',
        'address.line_1' => '2992 Eagle Drive',
        'address.line_2' => '',
        'address.suburb' => 'Detroit',
        'address.state' => 'MI',
        'address.postcode' => '48219'
    ]);

    $person = $person->undot();

    $person->toArray();

    /*
        [
            "name" => [
                "first_name" => "Marie",
                "last_name" => "Valentine",
            ],
            "address" => [
                "line_1" => "2992 Eagle Drive",
                "line_2" => "",
                "suburb" => "Detroit",
                "state" => "MI",
                "postcode" => "48219",
            ],
        ]
    */

<a name="method-union"></a>
#### `union()` {.collection-method}

`union` メソッドは、指定された配列をコレクションに追加します。指定された配列に元のコレクションに既に存在するキーが含まれている場合は、元のコレクションの値が優先されます。

    $collection = collect([1 => ['a'], 2 => ['b']]);

    $union = $collection->union([3 => ['c'], 1 => ['d']]);

    $union->all();

    // [1 => ['a'], 2 => ['b'], 3 => ['c']]

<a name="method-unique"></a>
#### `unique()` {.collection-method}

`unique` メソッドは、コレクション内のすべての一意の項目を返します。返されたコレクションには元の配列キーが保持されているため、次の例では、[`values`](#method-values) メソッドを使用してキーを連続番号のインデックスにリセットします。

    $collection = collect([1, 1, 2, 2, 3, 4, 2]);

    $unique = $collection->unique();

    $unique->values()->all();

    // [1, 2, 3, 4]

ネストされた配列またはオブジェクトを扱う場合、一意性を決定するために使用されるキーを指定できます。

    $collection = collect([
        ['name' => 'iPhone 6', 'brand' => 'Apple', 'type' => 'phone'],
        ['name' => 'iPhone 5', 'brand' => 'Apple', 'type' => 'phone'],
        ['name' => 'Apple Watch', 'brand' => 'Apple', 'type' => 'watch'],
        ['name' => 'Galaxy S6', 'brand' => 'Samsung', 'type' => 'phone'],
        ['name' => 'Galaxy Gear', 'brand' => 'Samsung', 'type' => 'watch'],
    ]);

    $unique = $collection->unique('brand');

    $unique->values()->all();

    /*
        [
            ['name' => 'iPhone 6', 'brand' => 'Apple', 'type' => 'phone'],
            ['name' => 'Galaxy S6', 'brand' => 'Samsung', 'type' => 'phone'],
        ]
    */

最後に、独自のクロージャを `unique` メソッドに渡して、項目の一意性を決定する値を指定することもできます。

    $unique = $collection->unique(function (array $item) {
        return $item['brand'].$item['type'];
    });

    $unique->values()->all();

    /*
        [
            ['name' => 'iPhone 6', 'brand' => 'Apple', 'type' => 'phone'],
            ['name' => 'Apple Watch', 'brand' => 'Apple', 'type' => 'watch'],
            ['name' => 'Galaxy S6', 'brand' => 'Samsung', 'type' => 'phone'],
            ['name' => 'Galaxy Gear', 'brand' => 'Samsung', 'type' => 'watch'],
        ]
    */

`unique` メソッドは、項目値をチェックするときに「緩やかな」比較を使用します。つまり、整数値を持つ文字列は、同じ値の整数と等しいと見なされます。 「厳密な」比較を使用してフィルタリングするには、[`uniqueStrict`](#method-uniquestrict) メソッドを使用します。

> [!NOTE]  
> [Eloquent コレクション](/docs/{{version}}/eloquent-collections#method-unique) を使用すると、このメソッドの動作が変更されます。

<a name="method-uniquestrict"></a>
#### `uniqueStrict()` {.collection-method}

このメソッドには、[`unique`](#method-unique) メソッドと同じシグネチャがあります。ただし、すべての値は「厳密な」比較を使用して比較されます。

<a name="method-unless"></a>
#### `unless()` {.collection-method}

`unless` メソッドは、メソッドに指定された最初の引数が `true` と評価されない限り、指定されたコールバックを実行します。

    $collection = collect([1, 2, 3]);

    $collection->unless(true, function (Collection $collection) {
        return $collection->push(4);
    });

    $collection->unless(false, function (Collection $collection) {
        return $collection->push(5);
    });

    $collection->all();

    // [1, 2, 3, 5]

2 番目のコールバックを `unless` メソッドに渡すことができます。 2 番目のコールバックは、`unless` メソッドに指定された最初の引数が `true` と評価されたときに実行されます。

    $collection = collect([1, 2, 3]);

    $collection->unless(true, function (Collection $collection) {
        return $collection->push(4);
    }, function (Collection $collection) {
        return $collection->push(5);
    });

    $collection->all();

    // [1, 2, 3, 5]

`unless` の逆については、[`when`](#method-when) メソッドを参照してください。

<a name="method-unlessempty"></a>
#### `unlessEmpty()` {.collection-method}

[`whenNotEmpty`](#method-whennotempty) メソッドのエイリアス。

<a name="method-unlessnotempty"></a>
#### `unlessNotEmpty()` {.collection-method}

[`whenEmpty`](#method-whenempty) メソッドのエイリアス。

<a name="method-unwrap"></a>
#### `unwrap()` {.collection-method}

静的 `unwrap` メソッドは、該当する場合、指定された値からコレクションの基礎となる項目を返します。

    Collection::unwrap(collect('John Doe'));

    // ['John Doe']

    Collection::unwrap(['John Doe']);

    // ['John Doe']

    Collection::unwrap('John Doe');

    // 'John Doe'

<a name="method-value"></a>
#### `value()` {.collection-method}

`value` メソッドは、コレクションの最初の要素から指定された値を取得します。

    $collection = collect([
        ['product' => 'Desk', 'price' => 200],
        ['product' => 'Speaker', 'price' => 400],
    ]);

    $value = $collection->value('price');

    // 200

<a name="method-values"></a>
#### `values()` {.collection-method}

`values` メソッドは、キーが連続した整数にリセットされた新しいコレクションを返します。

    $collection = collect([
        10 => ['product' => 'Desk', 'price' => 200],
        11 => ['product' => 'Desk', 'price' => 200],
    ]);

    $values = $collection->values();

    $values->all();

    /*
        [
            0 => ['product' => 'Desk', 'price' => 200],
            1 => ['product' => 'Desk', 'price' => 200],
        ]
    */

<a name="method-when"></a>
#### `when()` {.collection-method}

`when` メソッドは、メソッドに指定された最初の引数が `true` と評価されると、指定されたコールバックを実行します。コレクション インスタンスと `when` メソッドに指定された最初の引数がクロージャに提供されます。

    $collection = collect([1, 2, 3]);

    $collection->when(true, function (Collection $collection, int $value) {
        return $collection->push(4);
    });

    $collection->when(false, function (Collection $collection, int $value) {
        return $collection->push(5);
    });

    $collection->all();

    // [1, 2, 3, 4]

2 番目のコールバックを `when` メソッドに渡すことができます。 2 番目のコールバックは、`when` メソッドに指定された最初の引数が `false` と評価されたときに実行されます。

    $collection = collect([1, 2, 3]);

    $collection->when(false, function (Collection $collection, int $value) {
        return $collection->push(4);
    }, function (Collection $collection) {
        return $collection->push(5);
    });

    $collection->all();

    // [1, 2, 3, 5]

`when` の逆については、[`unless`](#method-unless) メソッドを参照してください。

<a name="method-whenempty"></a>
#### `whenEmpty()` {.collection-method}

`whenEmpty` メソッドは、コレクションが空のときに指定されたコールバックを実行します。

    $collection = collect(['Michael', 'Tom']);

    $collection->whenEmpty(function (Collection $collection) {
        return $collection->push('Adam');
    });

    $collection->all();

    // ['Michael', 'Tom']


    $collection = collect();

    $collection->whenEmpty(function (Collection $collection) {
        return $collection->push('Adam');
    });

    $collection->all();

    // ['Adam']

2 番目のクロージャは、コレクションが空でない場合に実行される `whenEmpty` メソッドに渡すことができます。

    $collection = collect(['Michael', 'Tom']);

    $collection->whenEmpty(function (Collection $collection) {
        return $collection->push('Adam');
    }, function (Collection $collection) {
        return $collection->push('Taylor');
    });

    $collection->all();

    // ['Michael', 'Tom', 'Taylor']

`whenEmpty` の逆については、[`whenNotEmpty`](#method-whennotempty) メソッドを参照してください。

<a name="method-whennotempty"></a>
#### `whenNotEmpty()` {.collection-method}

`whenNotEmpty` メソッドは、コレクションが空でない場合に指定されたコールバックを実行します。

    $collection = collect(['michael', 'tom']);

    $collection->whenNotEmpty(function (Collection $collection) {
        return $collection->push('adam');
    });

    $collection->all();

    // ['michael', 'tom', 'adam']


    $collection = collect();

    $collection->whenNotEmpty(function (Collection $collection) {
        return $collection->push('adam');
    });

    $collection->all();

    // []

2 番目のクロージャは、コレクションが空のときに実行される `whenNotEmpty` メソッドに渡すことができます。

    $collection = collect();

    $collection->whenNotEmpty(function (Collection $collection) {
        return $collection->push('adam');
    }, function (Collection $collection) {
        return $collection->push('taylor');
    });

    $collection->all();

    // ['taylor']

`whenNotEmpty` の逆については、[`whenEmpty`](#method-whenempty) メソッドを参照してください。

<a name="method-where"></a>
#### `where()` {.collection-method}

`where` メソッドは、指定されたキーと値のペアによってコレクションをフィルターします。

    $collection = collect([
        ['product' => 'Desk', 'price' => 200],
        ['product' => 'Chair', 'price' => 100],
        ['product' => 'Bookcase', 'price' => 150],
        ['product' => 'Door', 'price' => 100],
    ]);

    $filtered = $collection->where('price', 100);

    $filtered->all();

    /*
        [
            ['product' => 'Chair', 'price' => 100],
            ['product' => 'Door', 'price' => 100],
        ]
    */

`where` メソッドは、項目値をチェックするときに「緩やかな」比較を使用します。つまり、整数値を持つ文字列は、同じ値の整数と等しいと見なされます。 「厳密な」比較を使用してフィルタリングするには、[`whereStrict`](#method-wherestrict) メソッドを使用します。

オプションで、比較演算子を 2 番目のパラメータとして渡すこともできます。サポートされている演算子は、「===」、「!==」、「!=」、「==」、「=」、「<>」、「>」、「<」、「>=」、および「<=」です。

    $collection = collect([
        ['name' => 'Jim', 'deleted_at' => '2019-01-01 00:00:00'],
        ['name' => 'Sally', 'deleted_at' => '2019-01-02 00:00:00'],
        ['name' => 'Sue', 'deleted_at' => null],
    ]);

    $filtered = $collection->where('deleted_at', '!=', null);

    $filtered->all();

    /*
        [
            ['name' => 'Jim', 'deleted_at' => '2019-01-01 00:00:00'],
            ['name' => 'Sally', 'deleted_at' => '2019-01-02 00:00:00'],
        ]
    */

<a name="method-wherestrict"></a>
#### `whereStrict()` {.collection-method}

このメソッドには、[`where`](#method-where) メソッドと同じシグネチャがあります。ただし、すべての値は「厳密な」比較を使用して比較されます。

<a name="method-wherebetween"></a>
#### `whereBetween()` {.collection-method}

`whereBetween` メソッドは、指定された項目値が指定された範囲内にあるかどうかを判断して、コレクションをフィルターします。

    $collection = collect([
        ['product' => 'Desk', 'price' => 200],
        ['product' => 'Chair', 'price' => 80],
        ['product' => 'Bookcase', 'price' => 150],
        ['product' => 'Pencil', 'price' => 30],
        ['product' => 'Door', 'price' => 100],
    ]);

    $filtered = $collection->whereBetween('price', [100, 200]);

    $filtered->all();

    /*
        [
            ['product' => 'Desk', 'price' => 200],
            ['product' => 'Bookcase', 'price' => 150],
            ['product' => 'Door', 'price' => 100],
        ]
    */

<a name="method-wherein"></a>
#### `whereIn()` {.collection-method}

`whereIn` メソッドは、指定された配列内に含まれる指定された項目値を持たない要素をコレクションから削除します。

    $collection = collect([
        ['product' => 'Desk', 'price' => 200],
        ['product' => 'Chair', 'price' => 100],
        ['product' => 'Bookcase', 'price' => 150],
        ['product' => 'Door', 'price' => 100],
    ]);

    $filtered = $collection->whereIn('price', [150, 200]);

    $filtered->all();

    /*
        [
            ['product' => 'Desk', 'price' => 200],
            ['product' => 'Bookcase', 'price' => 150],
        ]
    */

`whereIn` メソッドは、項目値をチェックするときに「緩やかな」比較を使用します。つまり、整数値を持つ文字列は、同じ値の整数と等しいと見なされます。 「厳密な」比較を使用してフィルタリングするには、[`whereInStrict`](#method-whereinstrict) メソッドを使用します。

<a name="method-whereinstrict"></a>
#### `whereInStrict()` {.collection-method}

このメソッドには、[`whereIn`](#method-wherein) メソッドと同じシグネチャがあります。ただし、すべての値は「厳密な」比較を使用して比較されます。

<a name="method-whereinstanceof"></a>
#### `whereInstanceOf()` {.collection-method}

`whereInstanceOf` メソッドは、指定されたクラス タイプでコレクションをフィルターします。

    use App\Models\User;
    use App\Models\Post;

    $collection = collect([
        new User,
        new User,
        new Post,
    ]);

    $filtered = $collection->whereInstanceOf(User::class);

    $filtered->all();

    // [App\Models\User, App\Models\User]

<a name="method-wherenotbetween"></a>
#### `whereNotBetween()` {.collection-method}

`whereNotBetween` メソッドは、指定された項目の値が指定された範囲外であるかどうかを判断して、コレクションをフィルターします。

    $collection = collect([
        ['product' => 'Desk', 'price' => 200],
        ['product' => 'Chair', 'price' => 80],
        ['product' => 'Bookcase', 'price' => 150],
        ['product' => 'Pencil', 'price' => 30],
        ['product' => 'Door', 'price' => 100],
    ]);

    $filtered = $collection->whereNotBetween('price', [100, 200]);

    $filtered->all();

    /*
        [
            ['product' => 'Chair', 'price' => 80],
            ['product' => 'Pencil', 'price' => 30],
        ]
    */

<a name="method-wherenotin"></a>
#### `whereNotIn()` {.collection-method}

`whereNotIn` メソッドは、指定された配列内に含まれる指定された項目値を持つ要素をコレクションから削除します。

    $collection = collect([
        ['product' => 'Desk', 'price' => 200],
        ['product' => 'Chair', 'price' => 100],
        ['product' => 'Bookcase', 'price' => 150],
        ['product' => 'Door', 'price' => 100],
    ]);

    $filtered = $collection->whereNotIn('price', [150, 200]);

    $filtered->all();

    /*
        [
            ['product' => 'Chair', 'price' => 100],
            ['product' => 'Door', 'price' => 100],
        ]
    */

`whereNotIn` メソッドは、項目値をチェックするときに「緩やかな」比較を使用します。つまり、整数値を持つ文字列は、同じ値の整数と等しいと見なされます。 「厳密な」比較を使用してフィルタリングするには、[`whereNotInStrict`](#method-wherenotinstrict) メソッドを使用します。

<a name="method-wherenotinstrict"></a>
#### `whereNotInStrict()` {.collection-method}

このメソッドには、[`whereNotIn`](#method-wherenotin) メソッドと同じシグネチャがあります。ただし、すべての値は「厳密な」比較を使用して比較されます。

<a name="method-wherenotnull"></a>
#### `whereNotNull()` {.collection-method}

`whereNotNull` メソッドは、指定されたキーが `null` ではないコレクションから項目を返します。

    $collection = collect([
        ['name' => 'Desk'],
        ['name' => null],
        ['name' => 'Bookcase'],
    ]);

    $filtered = $collection->whereNotNull('name');

    $filtered->all();

    /*
        [
            ['name' => 'Desk'],
            ['name' => 'Bookcase'],
        ]
    */

<a name="method-wherenull"></a>
#### `whereNull()` {.collection-method}

`whereNull` メソッドは、指定されたキーが `null` であるコレクションから項目を返します。

    $collection = collect([
        ['name' => 'Desk'],
        ['name' => null],
        ['name' => 'Bookcase'],
    ]);

    $filtered = $collection->whereNull('name');

    $filtered->all();

    /*
        [
            ['name' => null],
        ]
    */


<a name="method-wrap"></a>
#### `wrap()` {.collection-method}

静的 `wrap` メソッドは、該当する場合、指定された値をコレクションにラップします。

    use Illuminate\Support\Collection;

    $collection = Collection::wrap('John Doe');

    $collection->all();

    // ['John Doe']

    $collection = Collection::wrap(['John Doe']);

    $collection->all();

    // ['John Doe']

    $collection = Collection::wrap(collect('John Doe'));

    $collection->all();

    // ['John Doe']

<a name="method-zip"></a>
#### `zip()` {.collection-method}

`zip` メソッドは、指定された配列の値と、対応するインデックスの元のコレクションの値をマージします。

    $collection = collect(['Chair', 'Desk']);

    $zipped = $collection->zip([100, 200]);

    $zipped->all();

    // [['Chair', 100], ['Desk', 200]]

<a name="higher-order-messages"></a>
## 高次メッセージ (Higher Order Messages)

コレクションは、コレクションに対して一般的なアクションを実行するためのショートカットである「高次メッセージ」のサポートも提供します。高次メッセージを提供する収集メソッドは、[`average`](#method-average)、[`avg`](#method-avg)、[`contains`](#method-contains)、[`each`](#method-each)、[`every`](#method-every)、[`filter`](#method-filter)、[`first`](#method-first)、[`flatMap`](#method-flatmap)、[`groupBy`](#method-groupby)、[`keyBy`](#method-keyby)、[`map`](#method-map)、 [`max`](#method-max)、[`min`](#method-min)、[`partition`](#method-partition)、[`reject`](#method-reject)、[`skipUntil`](#method-skipuntil)、[`skipWhile`](#method-skipwhile)、[`some`](#method-some)、[`sortBy`](#method-sortby)、[`sortByDesc`](#method-sortbydesc)、[`sum`](#method-sum)、[`takeUntil`](#method-takeuntil)、 [`takeWhile`](#method-takewhile)、および[`unique`](#method-unique)。

各高次メッセージには、コレクション インスタンスの動的プロパティとしてアクセスできます。たとえば、`each` 上位メッセージを使用して、コレクション内の各オブジェクトのメソッドを呼び出してみましょう。

    use App\Models\User;

    $users = User::where('votes', '>', 500)->get();

    $users->each->markAsVip();

同様に、`sum` 上位メッセージを使用して、ユーザーのコレクションの「投票」の合計数を収集できます。

    $users = User::where('group', 'Development')->get();

    return $users->sum->votes;

<a name="lazy-collections"></a>
## レイジーコレクション (Lazy Collections)

<a name="lazy-collection-introduction"></a>
### 導入

> [!WARNING]  
> Laravel の遅延コレクションについて詳しく学ぶ前に、時間をかけて [PHP ジェネレーター](https://www.php.net/manual/en/language.generators.overview.php) についてよく理解してください。

すでに強力な `Collection` クラスを補足するために、`LazyCollection` クラスは PHP の [generators](https://www.php.net/manual/en/language.generators.overview.php) を利用して、メモリ使用量を低く抑えながら非常に大規模なデータセットを操作できるようにします。

たとえば、アプリケーションがログを解析するために Laravel の収集メソッドを利用しながら、数ギガバイトのログ ファイルを処理する必要があると想像してください。ファイル全体を一度にメモリに読み取る代わりに、遅延コレクションを使用して、特定の時点でファイルのごく一部のみをメモリに保持することができます。

    use App\Models\LogEntry;
    use Illuminate\Support\LazyCollection;

    LazyCollection::make(function () {
        $handle = fopen('log.txt', 'r');

        while (($line = fgets($handle)) !== false) {
            yield $line;
        }
    })->chunk(4)->map(function (array $lines) {
        return LogEntry::fromLines($lines);
    })->each(function (LogEntry $logEntry) {
        // Process the log entry...
    });

あるいは、10,000 の Eloquent モデルを反復処理する必要があると想像してください。従来の Laravel コレクションを使用する場合、10,000 個の Eloquent モデルすべてを同時にメモリにロードする必要があります。

    use App\Models\User;

    $users = User::all()->filter(function (User $user) {
        return $user->id > 500;
    });

ただし、クエリビルダの `cursor` メソッドは、`LazyCollection` インスタンスを返します。これにより、データベースに対して 1 つのクエリのみを実行できますが、同時にメモリにロードされた Eloquent モデルは 1 つだけになります。この例では、`filter` コールバックは、実際に各ユーザーを個別に反復処理するまで実行されず、メモリ使用量を大幅に削減できます。

    use App\Models\User;

    $users = User::cursor()->filter(function (User $user) {
        return $user->id > 500;
    });

    foreach ($users as $user) {
        echo $user->id;
    }

<a name="creating-lazy-collections"></a>
### 遅延コレクションの作成

遅延コレクション インスタンスを作成するには、PHP ジェネレーター関数をコレクションの `make` メソッドに渡す必要があります。

    use Illuminate\Support\LazyCollection;

    LazyCollection::make(function () {
        $handle = fopen('log.txt', 'r');

        while (($line = fgets($handle)) !== false) {
            yield $line;
        }
    });

<a name="the-enumerable-contract"></a>
### 数え切れないほどの契約

`Collection` クラスで使用できるほぼすべてのメソッドは、`LazyCollection` クラスでも使用できます。これらのクラスは両方とも、次のメソッドを定義する `Illuminate\Support\Enumerable` コントラクトを実装します。

<style>
    .collection-method-list > p {
        columns: 10.8em 3; -moz-columns: 10.8em 3; -webkit-columns: 10.8em 3;
    }

    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
</style>

<div class="collection-method-list" markdown="1">

[all](#method-all)
[average](#method-average)
[avg](#method-avg)
[chunk](#method-chunk)
[chunkWhile](#method-chunkwhile)
[collapse](#method-collapse)
[collect](#method-collect)
[combine](#method-combine)
[concat](#method-concat)
[contains](#method-contains)
[containsStrict](#method-containsstrict)
[count](#method-count)
[countBy](#method-countBy)
[crossJoin](#method-crossjoin)
[dd](#method-dd)
[diff](#method-diff)
[diffAssoc](#method-diffassoc)
[diffKeys](#method-diffkeys)
[dump](#method-dump)
[duplicates](#method-duplicates)
[duplicatesStrict](#method-duplicatesstrict)
[each](#method-each)
[eachSpread](#method-eachspread)
[every](#method-every)
[except](#method-except)
[filter](#method-filter)
[first](#method-first)
[firstOrFail](#method-first-or-fail)
[firstWhere](#method-first-where)
[flatMap](#method-flatmap)
[flatten](#method-flatten)
[flip](#method-flip)
[forPage](#method-forpage)
[get](#method-get)
[groupBy](#method-groupby)
[has](#method-has)
[implode](#method-implode)
[intersect](#method-intersect)
[intersectAssoc](#method-intersectAssoc)
[intersectByKeys](#method-intersectbykeys)
[isEmpty](#method-isempty)
[isNotEmpty](#method-isnotempty)
[join](#method-join)
[keyBy](#method-keyby)
[keys](#method-keys)
[last](#method-last)
[macro](#method-macro)
[make](#method-make)
[map](#method-map)
[mapInto](#method-mapinto)
[mapSpread](#method-mapspread)
[mapToGroups](#method-maptogroups)
[mapWithKeys](#method-mapwithkeys)
[max](#method-max)
[median](#method-median)
[merge](#method-merge)
[mergeRecursive](#method-mergerecursive)
[min](#method-min)
[mode](#method-mode)
[nth](#method-nth)
[only](#method-only)
[pad](#method-pad)
[partition](#method-partition)
[pipe](#method-pipe)
[pluck](#method-pluck)
[random](#method-random)
[reduce](#method-reduce)
[reject](#method-reject)
[replace](#method-replace)
[replaceRecursive](#method-replacerecursive)
[reverse](#method-reverse)
[search](#method-search)
[shuffle](#method-shuffle)
[skip](#method-skip)
[slice](#method-slice)
[sole](#method-sole)
[some](#method-some)
[sort](#method-sort)
[sortBy](#method-sortby)
[sortByDesc](#method-sortbydesc)
[sortKeys](#method-sortkeys)
[sortKeysDesc](#method-sortkeysdesc)
[split](#method-split)
[sum](#method-sum)
[take](#method-take)
[tap](#method-tap)
[times](#method-times)
[toArray](#method-toarray)
[toJson](#method-tojson)
[union](#method-union)
[unique](#method-unique)
[uniqueStrict](#method-uniquestrict)
[unless](#method-unless)
[unlessEmpty](#method-unlessempty)
[unlessNotEmpty](#method-unlessnotempty)
[unwrap](#method-unwrap)
[values](#method-values)
[when](#method-when)
[whenEmpty](#method-whenempty)
[whenNotEmpty](#method-whennotempty)
[where](#method-where)
[whereStrict](#method-wherestrict)
[whereBetween](#method-wherebetween)
[whereIn](#method-wherein)
[whereInStrict](#method-whereinstrict)
[whereInstanceOf](#method-whereinstanceof)
[whereNotBetween](#method-wherenotbetween)
[whereNotIn](#method-wherenotin)
[whereNotInStrict](#method-wherenotinstrict)
[wrap](#method-wrap)
[zip](#method-zip)

</div>

> [!WARNING]  
> コレクションを変更するメソッド (`shift`、`pop`、`prepend` など) は、`LazyCollection` クラスでは**使用できません**。

<a name="lazy-collection-methods"></a>
### 遅延収集メソッド

`Enumerable` コントラクトで定義されたメソッドに加えて、`LazyCollection` クラスには次のメソッドが含まれています。

<a name="method-takeUntilTimeout"></a>
#### `takeUntilTimeout()` {.collection-method}

`takeUntilTimeout` メソッドは、指定された時間まで値を列挙する新しい遅延コレクションを返します。その後、コレクションは列挙を停止します。

    $lazyCollection = LazyCollection::times(INF)
        ->takeUntilTimeout(now()->addMinute());

    $lazyCollection->each(function (int $number) {
        dump($number);

        sleep(1);
    });

    // 1
    // 2
    // ...
    // 58
    // 59

このメソッドの使用法を説明するために、カーソルを使用してデータベースから請求書を送信するアプリケーションを想像してください。 15 分ごとに実行し、最大 14 分間請求書のみを処理する [スケジュールされたタスク](/docs/{{version}}/scheduling) を定義できます。

    use App\Models\Invoice;
    use Illuminate\Support\Carbon;

    Invoice::pending()->cursor()
        ->takeUntilTimeout(
            Carbon::createFromTimestamp(LARAVEL_START)->add(14, 'minutes')
        )
        ->each(fn (Invoice $invoice) => $invoice->submit());

<a name="method-tapEach"></a>
#### `tapEach()` {.collection-method}

`each` メソッドは、コレクション内の各項目に対して指定されたコールバックをすぐに呼び出しますが、`tapEach` メソッドは、項目がリストから 1 つずつ取り出されるときにのみ、指定されたコールバックを呼び出します。

    // Nothing has been dumped so far...
    $lazyCollection = LazyCollection::times(INF)->tapEach(function (int $value) {
        dump($value);
    });

    // Three items are dumped...
    $array = $lazyCollection->take(3)->all();

    // 1
    // 2
    // 3

<a name="method-remember"></a>
#### `remember()` {.collection-method}

`remember` メソッドは、すでに列挙された値を記憶し、後続のコレクション列挙ではそれらの値を再度取得しない、新しい遅延コレクションを返します。

    // No query has been executed yet...
    $users = User::cursor()->remember();

    // The query is executed...
    // The first 5 users are hydrated from the database...
    $users->take(5)->all();

    // First 5 users come from the collection's cache...
    // The rest are hydrated from the database...
    $users->take(20)->all();

