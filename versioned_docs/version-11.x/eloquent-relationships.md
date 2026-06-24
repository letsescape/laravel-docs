<!-- # Eloquent: Relationships -->
# Eloquent: Relationships

- [Introduction](#introduction)
- [Defining Relationships](#defining-relationships)
    - [One to One / Has One](#one-to-one)
    - [One to Many / Has Many](#one-to-many)
    - [One to Many (Inverse) / Belongs To](#one-to-many-inverse)
    - [Has One of Many](#has-one-of-many)
    - [Has One Through](#has-one-through)
    - [Has Many Through](#has-many-through)
- [Scoped Relationships](#scoped-relationships)
- [Many to Many Relationships](#many-to-many)
    - [Retrieving Intermediate Table Columns](#retrieving-intermediate-table-columns)
    - [Filtering Queries via Intermediate Table Columns](#filtering-queries-via-intermediate-table-columns)
    - [Ordering Queries via Intermediate Table Columns](#ordering-queries-via-intermediate-table-columns)
    - [Defining Custom Intermediate Table Models](#defining-custom-intermediate-table-models)
- [Polymorphic Relationships](#polymorphic-relationships)
    - [One to One](#one-to-one-polymorphic-relations)
    - [One to Many](#one-to-many-polymorphic-relations)
    - [One of Many](#one-of-many-polymorphic-relations)
    - [Many to Many](#many-to-many-polymorphic-relations)
    - [Custom Polymorphic Types](#custom-polymorphic-types)
- [Dynamic Relationships](#dynamic-relationships)
- [Querying Relations](#querying-relations)
    - [Relationship Methods vs. Dynamic Properties](#relationship-methods-vs-dynamic-properties)
    - [Querying Relationship Existence](#querying-relationship-existence)
    - [Querying Relationship Absence](#querying-relationship-absence)
    - [Querying Morph To Relationships](#querying-morph-to-relationships)
- [Aggregating Related Models](#aggregating-related-models)
    - [Counting Related Models](#counting-related-models)
    - [Other Aggregate Functions](#other-aggregate-functions)
    - [Counting Related Models on Morph To Relationships](#counting-related-models-on-morph-to-relationships)
- [Eager Loading](#eager-loading)
    - [Constraining Eager Loads](#constraining-eager-loads)
    - [Lazy Eager Loading](#lazy-eager-loading)
    - [Preventing Lazy Loading](#preventing-lazy-loading)
- [Inserting and Updating Related Models](#inserting-and-updating-related-models)
    - [The `save` Method](#the-save-method)
    - [The `create` Method](#the-create-method)
    - [Belongs To Relationships](#updating-belongs-to-relationships)
    - [Many to Many Relationships](#updating-many-to-many-relationships)
- [Touching Parent Timestamps](#touching-parent-timestamps)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Database tables are often related to one another. For example, a blog post may have many comments or an order could be related to the user who placed it. Eloquent makes managing and working with these relationships easy, and supports a variety of common relationships: -->
데이터베이스 테이블은 서로 연관되어 있는 경우가 많습니다. 예를 들어, 블로그 글에는 여러 개의 댓글이 달릴 수 있고, 주문은 주문한 사용자와 연결되어 있습니다. Eloquent는 이러한 연관관계를 쉽게 관리하고 사용할 수 있도록 다양한 기본 연관관계를 제공합니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [One To One](#one-to-one)
- [One To Many](#one-to-many)
- [Many To Many](#many-to-many)
- [Has One Through](#has-one-through)
- [Has Many Through](#has-many-through)
- [One To One (Polymorphic)](#one-to-one-polymorphic-relations)
- [One To Many (Polymorphic)](#one-to-many-polymorphic-relations)
- [Many To Many (Polymorphic)](#many-to-many-polymorphic-relations)

<!-- </div> -->
</div>

<a name="defining-relationships"></a>
<!-- ## Defining Relationships -->
## Defining Relationships

<!-- Eloquent relationships are defined as methods on your Eloquent model classes. Since relationships also serve as powerful [query builders](/docs/11.x/queries), defining relationships as methods provides powerful method chaining and querying capabilities. For example, we may chain additional query constraints on this `posts` relationship: -->
Eloquent의 연관관계는 Eloquent 모델 클래스에서 메서드 형태로 정의합니다. 연관관계 메서드는 강력한 [query builders](/docs/11.x/queries) 역할도 하므로, 메서드 체이닝을 통해 다양한 질의 조건을 추가로 지정할 수 있습니다. 예를 들어, 아래와 같이 `posts` 연관관계에 추가 쿼리 제약을 체이닝할 수 있습니다.

```
$user->posts()->where('active', 1)->get();
```

<!-- But, before diving too deep into using relationships, let's learn how to define each type of relationship supported by Eloquent. -->
본격적으로 연관관계를 사용해보기 전에, Eloquent가 지원하는 각 연관관계의 정의 방법부터 살펴보겠습니다.

<a name="one-to-one"></a>
<!-- ### One to One / Has One -->
### One to One / Has One

<!-- A one-to-one relationship is a very basic type of database relationship. For example, a `User` model might be associated with one `Phone` model. To define this relationship, we will place a `phone` method on the `User` model. The `phone` method should call the `hasOne` method and return its result. The `hasOne` method is available to your model via the model's `Illuminate\Database\Eloquent\Model` base class: -->
일대일(One-to-One) 연관관계는 가장 기본적인 데이터베이스 관계입니다. 예를 들어, `User` 모델은 하나의 `Phone` 모델과 연결될 수 있습니다. 이 관계를 정의하려면 `User` 모델에 `phone` 메서드를 추가하고, 이 `phone` 메서드에서 `hasOne` 메서드를 호출해 반환하면 됩니다. `hasOne` 메서드는 모델의 부모 클래스인 `Illuminate\Database\Eloquent\Model`을 통해 제공됩니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOne;

class User extends Model
{
    /**
     * Get the phone associated with the user.
     */
    public function phone(): HasOne
    {
        return $this->hasOne(Phone::class);
    }
}
```

<!-- The first argument passed to the `hasOne` method is the name of the related model class. Once the relationship is defined, we may retrieve the related record using Eloquent's dynamic properties. Dynamic properties allow you to access relationship methods as if they were properties defined on the model: -->
`hasOne` 메서드의 첫 번째 인수로는 관련 모델 클래스명을 전달합니다. 연관관계를 정의한 후에는, Eloquent의 동적 속성(Dynamic Property) 기능을 이용해 관련 레코드를 바로 조회할 수 있습니다. 동적 속성은, 연관관계 메서드를 마치 모델의 속성처럼 접근할 수 있게 해주는 기능입니다.

```
$phone = User::find(1)->phone;
```

<!-- Eloquent determines the foreign key of the relationship based on the parent model name. In this case, the `Phone` model is automatically assumed to have a `user_id` foreign key. If you wish to override this convention, you may pass a second argument to the `hasOne` method: -->
Eloquent는 연관관계의 외래 키(foreign key)를 부모 모델의 이름을 기준으로 자동으로 결정합니다. 위 예시의 경우, `Phone` 모델에 기본적으로 `user_id`라는 외래 키가 있다고 간주합니다. 이 규칙을 변경하고 싶다면, `hasOne` 메서드의 두 번째 인수로 외래 키 이름을 지정할 수 있습니다.

```
return $this->hasOne(Phone::class, 'foreign_key');
```

<!-- Additionally, Eloquent assumes that the foreign key should have a value matching the primary key column of the parent. In other words, Eloquent will look for the value of the user's `id` column in the `user_id` column of the `Phone` record. If you would like the relationship to use a primary key value other than `id` or your model's `$primaryKey` property, you may pass a third argument to the `hasOne` method: -->
또한 Eloquent는 기본적으로 외래 키의 값은 부모 모델의 기본 키 컬럼(primary key) 값과 일치해야 한다고 가정합니다. 즉, Eloquent는 `Phone` 레코드의 `user_id` 컬럼 값이 사용자의 `id` 컬럼과 동일한지를 기준으로 연관관계를 찾습니다. 만약 기본 키 컬럼이 `id`가 아니거나, 모델의 `$primaryKey` 속성 이외의 값을 사용하고 싶다면, `hasOne` 메서드의 세 번째 인수로 로컬 키를 지정할 수 있습니다.

```
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
<!-- #### Defining the Inverse of the Relationship -->
#### Defining the Inverse of the Relationship

<!-- So, we can access the `Phone` model from our `User` model. Next, let's define a relationship on the `Phone` model that will let us access the user that owns the phone. We can define the inverse of a `hasOne` relationship using the `belongsTo` method: -->
이제 `User` 모델에서 `Phone` 모델을 조회할 수 있게 되었습니다. 다음으로, `Phone` 모델에서 이 전화번호의 소유자인 사용자를 조회할 수 있도록 역방향 연관관계를 정의해봅시다. 이때는 `hasOne`의 역방향인 `belongsTo` 메서드를 사용합니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Phone extends Model
{
    /**
     * Get the user that owns the phone.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
```

<!-- When invoking the `user` method, Eloquent will attempt to find a `User` model that has an `id` which matches the `user_id` column on the `Phone` model. -->
`user` 메서드를 호출하면, Eloquent는 `Phone` 모델의 `user_id` 컬럼 값과 일치하는 `id` 값을 가진 `User` 모델을 찾아 반환합니다.

<!-- Eloquent determines the foreign key name by examining the name of the relationship method and suffixing the method name with `_id`. So, in this case, Eloquent assumes that the `Phone` model has a `user_id` column. However, if the foreign key on the `Phone` model is not `user_id`, you may pass a custom key name as the second argument to the `belongsTo` method: -->
Eloquent는 연관관계 메서드의 이름에 `_id`를 붙여 외래 키 이름을 추론합니다. 즉, 위 예제에서는 `Phone` 모델에 `user_id` 컬럼이 있다고 간주합니다. 만약 `Phone` 모델의 실제 외래 키가 `user_id`가 아니라면, `belongsTo`의 두 번째 인수로 외래 키를 지정할 수 있습니다.

```
/**
 * Get the user that owns the phone.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

<!-- If the parent model does not use `id` as its primary key, or you wish to find the associated model using a different column, you may pass a third argument to the `belongsTo` method specifying the parent table's custom key: -->
마찬가지로, 상위(부모) 모델의 기본 키가 `id`가 아니거나, 다른 컬럼을 기준으로 부모 모델을 찾고 싶다면, `belongsTo`의 세 번째 인수로 상위 테이블의 사용자 정의 키를 전달할 수 있습니다.

```
/**
 * Get the user that owns the phone.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a name="one-to-many"></a>
<!-- ### One to Many / Has Many -->
### One to Many / Has Many

<!-- A one-to-many relationship is used to define relationships where a single model is the parent to one or more child models. For example, a blog post may have an infinite number of comments. Like all other Eloquent relationships, one-to-many relationships are defined by defining a method on your Eloquent model: -->
일대다(One-to-Many) 연관관계는 하나의 모델이 여러 개의 하위 모델을 소유할 때 사용합니다. 예를 들어, 블로그 글에는 무한정 많은 댓글이 달릴 수 있습니다. 다른 Eloquent 연관관계와 마찬가지로, 일대다 관계 역시 모델에 메서드를 정의해서 구현합니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * Get the comments for the blog post.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```

<!-- Remember, Eloquent will automatically determine the proper foreign key column for the `Comment` model. By convention, Eloquent will take the "snake case" name of the parent model and suffix it with `_id`. So, in this example, Eloquent will assume the foreign key column on the `Comment` model is `post_id`. -->
Eloquent는 `Comment` 모델의 적절한 외래 키 컬럼을 자동으로 결정합니다. 기본적으로는 상위 모델의 이름(스네이크 케이스 처리)에 `_id`를 붙여 외래 키 이름을 만듭니다. 즉, 예시에서는 `Comment` 모델에 `post_id` 컬럼이 있다고 가정합니다.

<!-- Once the relationship method has been defined, we can access the [collection](/docs/11.x/eloquent-collections) of related comments by accessing the `comments` property. Remember, since Eloquent provides "dynamic relationship properties", we can access relationship methods as if they were defined as properties on the model: -->
연관관계 메서드를 정의한 후에는, `comments` 속성을 사용해 관련 댓글들의 [collection](/docs/11.x/eloquent-collections)을 조회할 수 있습니다. 여기서도 Eloquent가 제공하는 동적 속성(Dynamic Property)을 통해, 연관관계 메서드를 마치 모델에 정의된 속성처럼 접근할 수 있습니다.

```
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    // ...
}
```

<!-- Since all relationships also serve as query builders, you may add further constraints to the relationship query by calling the `comments` method and continuing to chain conditions onto the query: -->
모든 연관관계는 쿼리 빌더 역할을 하기 때문에, `comments` 메서드를 통해 쿼리 제약 조건을 추가로 체이닝할 수도 있습니다.

```
$comment = Post::find(1)->comments()
    ->where('title', 'foo')
    ->first();
```

<!-- Like the `hasOne` method, you may also override the foreign and local keys by passing additional arguments to the `hasMany` method: -->
`hasOne` 메서드와 마찬가지로, `hasMany`에도 추가 인수를 넘겨 외래 키, 로컬 키를 직접 지정할 수 있습니다.

```
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="automatically-hydrating-parent-models-on-children"></a>
<!-- #### Automatically Hydrating Parent Models on Children -->
#### Automatically Hydrating Parent Models on Children

<!-- Even when utilizing Eloquent eager loading, "N + 1" query problems can arise if you try to access the parent model from a child model while looping through the child models: -->
Eloquent에서 eager loading을 사용하더라도, 자식 모델에서 부모 모델을 참조하는 과정에서 "N + 1" 쿼리 문제가 발생할 수 있습니다. 예를 들어, 다음과 같이 반복문에서 자식 모델의 부모 모델에 접근하면 문제가 생길 수 있습니다.

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->post->title;
    }
}
```

<!-- In the example above, an "N + 1" query problem has been introduced because, even though comments were eager loaded for every `Post` model, Eloquent does not automatically hydrate the parent `Post` on each child `Comment` model. -->
위 예시에서는 각 `Post` 모델에 대해 댓글이 eager loading되지만, 각 자식 `Comment` 모델에는 부모인 `Post` 모델이 자동으로 할당되지 않기 때문에 "N + 1" 쿼리 문제가 발생합니다.

<!-- If you would like Eloquent to automatically hydrate parent models onto their children, you may invoke the `chaperone` method when defining a `hasMany` relationship: -->
자식 모델에 부모 모델을 자동으로 할당하고 싶다면, `hasMany` 연관관계를 정의할 때 `chaperone` 메서드를 호출하면 됩니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * Get the comments for the blog post.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class)->chaperone();
    }
}
```

<!-- Or, if you would like to opt-in to automatic parent hydration at run time, you may invoke the `chaperone` model when eager loading the relationship: -->
또는, 런타임에서 관계를 eager load할 때 `chaperone` 메서드를 체이닝하여 부모 자동 할당 기능을 사용할 수도 있습니다.

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-to-many-inverse"></a>
<!-- ### One to Many (Inverse) / Belongs To -->
### One to Many (Inverse) / Belongs To

<!-- Now that we can access all of a post's comments, let's define a relationship to allow a comment to access its parent post. To define the inverse of a `hasMany` relationship, define a relationship method on the child model which calls the `belongsTo` method: -->
이제 특정 게시글의 모든 댓글을 조회할 수 있게 되었으니, 이번에는 댓글별로 자신의 부모 게시글을 조회할 수 있는 관계를 정의해보겠습니다. `hasMany` 관계의 역방향 연관관계는, 자식 모델에서 `belongsTo` 메서드를 사용해 관계 메서드를 정의하면 됩니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * Get the post that owns the comment.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

<!-- Once the relationship has been defined, we can retrieve a comment's parent post by accessing the `post` "dynamic relationship property": -->
관계를 정의한 뒤에는, 댓글 인스턴스에서 `post` "동적 연관관계 속성"으로 부모 게시글을 바로 조회할 수 있습니다.

```
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

<!-- In the example above, Eloquent will attempt to find a `Post` model that has an `id` which matches the `post_id` column on the `Comment` model. -->
위 예시에서, Eloquent는 `Comment` 모델의 `post_id` 컬럼 값과 일치하는 `id` 값을 가진 `Post` 모델을 찾아 반환합니다.

<!-- Eloquent determines the default foreign key name by examining the name of the relationship method and suffixing the method name with a `_` followed by the name of the parent model's primary key column. So, in this example, Eloquent will assume the `Post` model's foreign key on the `comments` table is `post_id`. -->
Eloquent는 관계 메서드의 이름에 `_`와 부모 모델 기본 키 컬럼명을 붙여 외래 키를 추론합니다. 즉, 여기서는 `comments` 테이블에 대한 `Post` 모델의 외래 키가 `post_id`라고 간주합니다.

<!-- However, if the foreign key for your relationship does not follow these conventions, you may pass a custom foreign key name as the second argument to the `belongsTo` method: -->
만약 외래 키 컬럼 이름이 이 규칙을 따르지 않는다면, `belongsTo` 메서드의 두 번째 인수로 외래 키 이름을 직접 지정할 수 있습니다.

```
/**
 * Get the post that owns the comment.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

<!-- If your parent model does not use `id` as its primary key, or you wish to find the associated model using a different column, you may pass a third argument to the `belongsTo` method specifying your parent table's custom key: -->
부모 모델의 기본 키가 `id`가 아닌 다른 컬럼이거나, 다른 컬럼으로 부모 모델을 찾고 싶은 경우에는, `belongsTo` 메서드의 세 번째 인수로 부모 테이블의 키를 지정할 수 있습니다.

```
/**
 * Get the post that owns the comment.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
<!-- #### Default Models -->
#### Default Models

<!-- The `belongsTo`, `hasOne`, `hasOneThrough`, and `morphOne` relationships allow you to define a default model that will be returned if the given relationship is `null`. This pattern is often referred to as the [Null Object pattern](https://en.wikipedia.org/wiki/Null_Object_pattern) and can help remove conditional checks in your code. In the following example, the `user` relation will return an empty `App\Models\User` model if no user is attached to the `Post` model: -->
`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 연관관계에서는, 관계 결과가 `null`일 경우 대신 반환될 기본(default) 모델을 정의할 수 있습니다. 이 패턴은 [Null Object pattern](https://en.wikipedia.org/wiki/Null_Object_pattern)이라고도 하며, 조건문을 줄여 코드를 간결하게 만들 수 있습니다. 아래 예시에서, `Post` 모델에 연결된 사용자가 없을 경우, `user` 연관관계는 빈 `App\Models\User` 모델을 반환하게 됩니다.

```
/**
 * Get the author of the post.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```

<!-- To populate the default model with attributes, you may pass an array or closure to the `withDefault` method: -->
기본 모델의 속성 값을 미리 채우고 싶다면, `withDefault` 메서드에 배열이나 클로저를 전달할 수 있습니다.

```
/**
 * Get the author of the post.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

/**
 * Get the author of the post.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault(function (User $user, Post $post) {
        $user->name = 'Guest Author';
    });
}
```

<a name="querying-belongs-to-relationships"></a>
<!-- #### Querying Belongs To Relationships -->
#### Querying Belongs To Relationships

<!-- When querying for the children of a "belongs to" relationship, you may manually build the `where` clause to retrieve the corresponding Eloquent models: -->
"Belongs To" 관계의 자식 모델들(즉, 특정 상위 모델에 소속된 모든 하위 모델)을 쿼리할 때는, 다음과 같이 수동으로 `where` 조건을 작성할 수 있습니다.

```
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

<!-- However, you may find it more convenient to use the `whereBelongsTo` method, which will automatically determine the proper relationship and foreign key for the given model: -->
하지만, Laravel의 `whereBelongsTo` 메서드를 사용하면, 적절한 연관관계와 외래 키를 자동으로 판별해줘서 더욱 편리하게 쿼리를 작성할 수 있습니다.

```
$posts = Post::whereBelongsTo($user)->get();
```

<!-- You may also provide a [collection](/docs/11.x/eloquent-collections) instance to the `whereBelongsTo` method. When doing so, Laravel will retrieve models that belong to any of the parent models within the collection: -->
또한, `whereBelongsTo` 메서드에는 [collection](/docs/11.x/eloquent-collections) 인스턴스를 바로 전달할 수 있습니다. 이럴 경우, 컬렉션에 포함된 모든 부모 모델에 소속된 하위 모델을 한 번에 불러옵니다.

```
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

<!-- By default, Laravel will determine the relationship associated with the given model based on the class name of the model; however, you may specify the relationship name manually by providing it as the second argument to the `whereBelongsTo` method: -->
기본적으로 Laravel은 전달된 모델의 클래스명을 기준으로 적절한 연관관계를 찾지만, `whereBelongsTo` 메서드의 두 번째 인수로 연관관계 이름을 직접 지정할 수도 있습니다.

```
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
<!-- ### Has One of Many -->
### Has One of Many

<!-- Sometimes a model may have many related models, yet you want to easily retrieve the "latest" or "oldest" related model of the relationship. For example, a `User` model may be related to many `Order` models, but you want to define a convenient way to interact with the most recent order the user has placed. You may accomplish this using the `hasOne` relationship type combined with the `ofMany` methods: -->
때때로 하나의 모델이 여러 개의 관련 모델을 가질 수 있지만, 연관된 모델 중 가장 최근(recent) 또는 가장 오래된(oldest) 단일 모델만 쉽고 빠르게 가져오고 싶을 때가 있습니다. 예를 들어, `User` 모델은 여러 개의 `Order` 모델과 연관될 수 있지만, 사용자가 마지막으로 주문한 가장 최근 주문 건에 쉽게 접근하고 싶은 경우가 있습니다. 이럴 때는 `hasOne` 관계와 `ofMany` 계열 메서드를 조합해서 사용할 수 있습니다.

```php
/**
 * Get the user's most recent order.
 */
public function latestOrder(): HasOne
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

<!-- Likewise, you may define a method to retrieve the "oldest", or first, related model of a relationship: -->
마찬가지로, "가장 오래된"(first) 연관 모델을 가져오는 메서드도 다음과 같이 정의할 수 있습니다.

```php
/**
 * Get the user's oldest order.
 */
public function oldestOrder(): HasOne
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

<!-- By default, the `latestOfMany` and `oldestOfMany` methods will retrieve the latest or oldest related model based on the model's primary key, which must be sortable. However, sometimes you may wish to retrieve a single model from a larger relationship using a different sorting criteria. -->
`latestOfMany`와 `oldestOfMany` 메서드는 기본적으로 모델의 기본 키(정렬 가능한 값 기준)로 가장 최근 또는 오래된 모델을 찾습니다. 하지만 때로는 다른 기준으로 정렬해 단일 모델을 가져오고 싶을 수 있습니다.

<!-- For example, using the `ofMany` method, you may retrieve the user's most expensive order. The `ofMany` method accepts the sortable column as its first argument and which aggregate function (`min` or `max`) to apply when querying for the related model: -->
예를 들어, `ofMany` 메서드를 사용해서 사용자의 "가장 비싼" 주문 건을 조회할 수도 있습니다. 이때 `ofMany`의 첫 번째 인수로 정렬 대상 컬럼, 두 번째 인수로 집계 함수(`min` 또는 `max`)를 전달합니다.

```php
/**
 * Get the user's largest order.
 */
public function largestOrder(): HasOne
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```

> [!WARNING]
> PostgreSQL은 UUID 컬럼에 대해 `MAX` 함수를 지원하지 않으므로, PostgreSQL UUID 컬럼을 사용하는 환경에서는 one-of-many 관계를 사용할 수 없습니다.

<a name="converting-many-relationships-to-has-one-relationships"></a>
<!-- #### Converting "Many" Relationships to Has One Relationships -->
#### Converting "Many" Relationships to Has One Relationships

<!-- Often, when retrieving a single model using the `latestOfMany`, `oldestOfMany`, or `ofMany` methods, you already have a "has many" relationship defined for the same model. For convenience, Laravel allows you to easily convert this relationship into a "has one" relationship by invoking the `one` method on the relationship: -->
이미 "has many" 연관관계가 정의되어 있을 때, `latestOfMany`, `oldestOfMany`, `ofMany`와 같은 메서드를 통해 단일 모델을 불러오는 패턴이 자주 필요하다면, Laravel에서는 기존의 "has many" 관계를 간단히 "has one" 관계로 변환할 수 있습니다. 이를 위해 관계에서 `one` 메서드를 호출하면 됩니다.

```php
/**
 * Get the user's orders.
 */
public function orders(): HasMany
{
    return $this->hasMany(Order::class);
}

/**
 * Get the user's largest order.
 */
public function largestOrder(): HasOne
{
    return $this->orders()->one()->ofMany('price', 'max');
}
```

<a name="advanced-has-one-of-many-relationships"></a>
<!-- #### Advanced Has One of Many Relationships -->
#### Advanced Has One of Many Relationships

<!-- It is possible to construct more advanced "has one of many" relationships. For example, a `Product` model may have many associated `Price` models that are retained in the system even after new pricing is published. In addition, new pricing data for the product may be able to be published in advance to take effect at a future date via a `published_at` column. -->
조금 더 복잡한 "has one of many" 관계도 정의할 수 있습니다. 예를 들어, `Product` 모델에는 여러 개의 `Price` 모델이 연관되어 있으며, 신제품 가격이 미리 등록되어 미래 시점에 적용될 수도 있습니다(`published_at` 컬럼 참고). 이런 상황에서는, 아직 적용되지 않은 미래 가격은 제외하고, 가장 마지막에 등록된(발행일이 현재보다 이전인) 가격 중, 발행일이 같으면 ID가 큰 가격을 가져오고 싶을 수 있습니다.

<!-- So, in summary, we need to retrieve the latest published pricing where the published date is not in the future. In addition, if two prices have the same published date, we will prefer the price with the greatest ID. To accomplish this, we must pass an array to the `ofMany` method that contains the sortable columns which determine the latest price. In addition, a closure will be provided as the second argument to the `ofMany` method. This closure will be responsible for adding additional publish date constraints to the relationship query: -->
이럴 때는, `ofMany` 메서드에 배열 형태로 여러 기준 컬럼을 지정하고, `ofMany` 메서드의 두 번째 인수로 Publish Date에 대한 추가 제약이 포함된 클로저를 전달해서 복잡한 관계를 정의할 수 있습니다.

```php
/**
 * Get the current pricing for the product.
 */
public function currentPricing(): HasOne
{
    return $this->hasOne(Price::class)->ofMany([
        'published_at' => 'max',
        'id' => 'max',
    ], function (Builder $query) {
        $query->where('published_at', '<', now());
    });
}
```

<a name="has-one-through"></a>
<!-- ### Has One Through -->
### Has One Through

<!-- The "has-one-through" relationship defines a one-to-one relationship with another model. However, this relationship indicates that the declaring model can be matched with one instance of another model by proceeding _through_ a third model. -->
"has-one-through" 관계는, 한 모델이 다른 모델과 일대일 연관관계를 가지되, _중간 모델을 거쳐서_ 최종 모델과 연결되는 구조를 의미합니다.

<!-- For example, in a vehicle repair shop application, each `Mechanic` model may be associated with one `Car` model, and each `Car` model may be associated with one `Owner` model. While the mechanic and the owner have no direct relationship within the database, the mechanic can access the owner _through_ the `Car` model. Let's look at the tables necessary to define this relationship: -->
예를 들어, 차량 정비소 애플리케이션에서, 각각의 `Mechanic`(정비공) 모델은 하나의 `Car`(자동차) 모델과 연결되어 있고, 각각의 `Car`는 하나의 `Owner`(차주) 모델과 연결될 수 있습니다. 이처럼 정비공과 차주는 데이터베이스상 직접 연결되어 있지 않지만, 정비공은 `Car` 모델을 _경유해서_ 차주에 접근할 수 있습니다. 아래는 이런 관계를 구성하는 테이블 예시입니다.

```
mechanics
    id - integer
    name - string

cars
    id - integer
    model - string
    mechanic_id - integer

owners
    id - integer
    name - string
    car_id - integer
```

<!-- Now that we have examined the table structure for the relationship, let's define the relationship on the `Mechanic` model: -->
테이블 구조를 확인했으니, 이제 `Mechanic` 모델에 관계를 정의해봅니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOneThrough;

class Mechanic extends Model
{
    /**
     * Get the car's owner.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```

<!-- The first argument passed to the `hasOneThrough` method is the name of the final model we wish to access, while the second argument is the name of the intermediate model. -->
`hasOneThrough` 메서드의 첫 번째 인수는 최종적으로 접근하고자 하는 모델, 두 번째 인수는 중간에 거치는 모델입니다.

<!-- Or, if the relevant relationships have already been defined on all of the models involved in the relationship, you may fluently define a "has-one-through" relationship by invoking the `through` method and supplying the names of those relationships. For example, if the `Mechanic` model has a `cars` relationship and the `Car` model has an `owner` relationship, you may define a "has-one-through" relationship connecting the mechanic and the owner like so: -->
또는, 이미 각 모델에 관계가 정의되어 있다면, `through` 메서드에 관계 이름을 전달해 좀 더 간결하게 Has One Through 관계를 정의할 수도 있습니다. 예를 들어, `Mechanic` 모델에 `cars` 관계가 있고, `Car` 모델에 `owner` 관계가 있다면, 아래와 같이 두 가지 방식으로 정의할 수 있습니다.

```php
// String based syntax...
return $this->through('cars')->has('owner');

// Dynamic syntax...
return $this->throughCars()->hasOwner();
```

<a name="has-one-through-key-conventions"></a>
<!-- #### Key Conventions -->
#### Key Conventions

<!-- Typical Eloquent foreign key conventions will be used when performing the relationship's queries. If you would like to customize the keys of the relationship, you may pass them as the third and fourth arguments to the `hasOneThrough` method. The third argument is the name of the foreign key on the intermediate model. The fourth argument is the name of the foreign key on the final model. The fifth argument is the local key, while the sixth argument is the local key of the intermediate model: -->
관계 쿼리를 수행할 때는 일반적인 Eloquent의 외래 키 명명 규칙이 적용됩니다. 하지만, 관계의 키를 직접 지정하고 싶다면 `hasOneThrough` 메서드의 세 번째, 네 번째 인수로 전달할 수 있습니다. 세 번째 인수는 중간 테이블의 외래 키, 네 번째 인수는 마지막 테이블의 외래 키입니다. 다섯 번째, 여섯 번째 인수는 각각 기점(로컬) 테이블, 중간 테이블의 로컬 키입니다.

```
class Mechanic extends Model
{
    /**
     * Get the car's owner.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(
            Owner::class,
            Car::class,
            'mechanic_id', // Foreign key on the cars table...
            'car_id', // Foreign key on the owners table...
            'id', // Local key on the mechanics table...
            'id' // Local key on the cars table...
        );
    }
}
```

<!-- Or, as discussed earlier, if the relevant relationships have already been defined on all of the models involved in the relationship, you may fluently define a "has-one-through" relationship by invoking the `through` method and supplying the names of those relationships. This approach offers the advantage of reusing the key conventions already defined on the existing relationships: -->
앞서 설명한 것처럼, 이미 각 모델에 관계가 정의되어 있다면, `through` 메서드에 관계 이름을 전달해 더욱 간결하게 Has One Through 관계를 구현할 수도 있습니다. 이 방식은 기존에 정의된 키 규칙을 재사용할 수 있다는 점이 장점입니다.

```php
// String based syntax...
return $this->through('cars')->has('owner');

// Dynamic syntax...
return $this->throughCars()->hasOwner();
```

<a name="has-many-through"></a>

<!-- ### Has Many Through -->
### Has Many Through

<!-- The "has-many-through" relationship provides a convenient way to access distant relations via an intermediate relation. For example, let's assume we are building a deployment platform like [Laravel Vapor](https://vapor.laravel.com). A `Project` model might access many `Deployment` models through an intermediate `Environment` model. Using this example, you could easily gather all deployments for a given project. Let's look at the tables required to define this relationship: -->
"has-many-through" 관계는 중간 관계를 통해 먼 거리에 있는 연관 관계의 데이터를 쉽게 조회할 수 있게 해줍니다. 예를 들어, [Laravel Vapor](https://vapor.laravel.com)와 같은 배포 플랫폼을 만든다고 가정해보겠습니다. 이때 `Project` 모델은 중간에 위치한 `Environment` 모델을 통해 여러 개의 `Deployment` 모델에 접근할 수 있습니다. 이 구조를 활용하면 하나의 프로젝트에 속한 모든 배포 정보를 손쉽게 조회할 수 있습니다. 이 관계를 정의하기 위해 필요한 데이터베이스 테이블들은 다음과 같습니다.

```
projects
    id - integer
    name - string

environments
    id - integer
    project_id - integer
    name - string

deployments
    id - integer
    environment_id - integer
    commit_hash - string
```

<!-- Now that we have examined the table structure for the relationship, let's define the relationship on the `Project` model: -->
이제 테이블 구조를 살펴보았으니, `Project` 모델에서 이 관계를 어떻게 정의할 수 있는지 알아보겠습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasManyThrough;

class Project extends Model
{
    /**
     * Get all of the deployments for the project.
     */
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(Deployment::class, Environment::class);
    }
}
```

<!-- The first argument passed to the `hasManyThrough` method is the name of the final model we wish to access, while the second argument is the name of the intermediate model. -->
`hasManyThrough` 메서드의 첫 번째 인수는 실제로 최종적으로 접근하고 싶은 모델이며, 두 번째 인수는 중간에 위치한 모델을 지정합니다.

<!-- Or, if the relevant relationships have already been defined on all of the models involved in the relationship, you may fluently define a "has-many-through" relationship by invoking the `through` method and supplying the names of those relationships. For example, if the `Project` model has a `environments` relationship and the `Environment` model has a `deployments` relationship, you may define a "has-many-through" relationship connecting the project and the deployments like so: -->
또는, 연관된 모든 모델에 이미 관계 메서드가 정의되어 있다면, `through` 메서드에 관계 명을 전달하여 더욱 간결하게 "has-many-through" 관계를 정의할 수 있습니다. 예를 들어, 만약 `Project` 모델에 `environments` 관계가 있고, `Environment` 모델에 `deployments` 관계가 있다면, 다음과 같이 프로젝트와 배포 사이의 "has-many-through" 관계를 정의할 수 있습니다.

```php
// String based syntax...
return $this->through('environments')->has('deployments');

// Dynamic syntax...
return $this->throughEnvironments()->hasDeployments();
```

<!-- Though the `Deployment` model's table does not contain a `project_id` column, the `hasManyThrough` relation provides access to a project's deployments via `$project->deployments`. To retrieve these models, Eloquent inspects the `project_id` column on the intermediate `Environment` model's table. After finding the relevant environment IDs, they are used to query the `Deployment` model's table. -->
`Deployment` 모델의 테이블에는 `project_id` 컬럼이 존재하지 않지만, `hasManyThrough` 관계를 이용하면 `$project->deployments`를 통해 프로젝트에 속한 배포 정보를 조회할 수 있습니다. 이때 Eloquent는 중간에 위치한 `Environment` 모델의 테이블에서 `project_id` 컬럼을 활용해 환경 ID 목록을 찾은 뒤, 해당 환경 ID로 `Deployment` 테이블을 조회하게 됩니다.

<a name="has-many-through-key-conventions"></a>
<!-- #### Key Conventions -->
#### Key Conventions

<!-- Typical Eloquent foreign key conventions will be used when performing the relationship's queries. If you would like to customize the keys of the relationship, you may pass them as the third and fourth arguments to the `hasManyThrough` method. The third argument is the name of the foreign key on the intermediate model. The fourth argument is the name of the foreign key on the final model. The fifth argument is the local key, while the sixth argument is the local key of the intermediate model: -->
관계형 쿼리를 실행할 때는 Eloquent의 기본 외래 키 명명 규칙이 사용됩니다. 만약 관계의 키를 직접 지정하고 싶다면, `hasManyThrough` 메서드의 세 번째 및 네 번째 인수로 키 이름을 전달하면 됩니다. 세 번째 인수는 중간 테이블의 외래 키, 네 번째 인수는 최종 테이블의 외래 키, 다섯 번째 인수는 로컬 키, 여섯 번째 인수는 중간 모델의 로컬 키입니다.

```
class Project extends Model
{
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(
            Deployment::class,
            Environment::class,
            'project_id', // Foreign key on the environments table...
            'environment_id', // Foreign key on the deployments table...
            'id', // Local key on the projects table...
            'id' // Local key on the environments table...
        );
    }
}
```

<!-- Or, as discussed earlier, if the relevant relationships have already been defined on all of the models involved in the relationship, you may fluently define a "has-many-through" relationship by invoking the `through` method and supplying the names of those relationships. This approach offers the advantage of reusing the key conventions already defined on the existing relationships: -->
또 앞서 설명한 것처럼, 모든 모델에 필요한 관계가 이미 정의되어 있다면, `through` 메서드에 관계명을 전달해 더욱 간단하게 "has-many-through" 관계를 설정할 수 있습니다. 이 방법을 사용하면 기존에 정의된 관계의 키 명명 규칙도 재활용할 수 있다는 장점이 있습니다.

```php
// String based syntax...
return $this->through('environments')->has('deployments');

// Dynamic syntax...
return $this->throughEnvironments()->hasDeployments();
```

<a name="scoped-relationships"></a>
<!-- ### Scoped Relationships -->
### Scoped Relationships

<!-- It's common to add additional methods to models that constrain relationships. For example, you might add a `featuredPosts` method to a `User` model which constrains the broader `posts` relationship with an additional `where` constraint: -->
모델에 조건이 적용된 관계 메서드를 추가하는 경우가 자주 있습니다. 예를 들어, `User` 모델에 `posts` 관계가 있다고 할 때, 여기에 추가적인 `where` 조건을 적용하여 특정 조건의 `featuredPosts` 메서드를 만들 수 있습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * Get the user's posts.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class)->latest();
    }

    /**
     * Get the user's featured posts.
     */
    public function featuredPosts(): HasMany
    {
        return $this->posts()->where('featured', true);
    }
}
```

<!-- However, if you attempt to create a model via the `featuredPosts` method, its `featured` attribute would not be set to `true`. If you would like to create models via relationship methods and also specify attributes that should be added to all models created via that relationship, you may use the `withAttributes` method when building the relationship query: -->
하지만 이렇게 정의된 `featuredPosts` 메서드로 새로운 모델을 생성할 경우, `featured` 속성이 `true`로 자동 설정되지 않습니다. 만약 관계 메서드를 통해 모델을 생성하면서도 해당 관계로 만들어진 모든 모델에 특정 속성을 자동으로 지정하고 싶다면, 관계 쿼리를 구성할 때 `withAttributes` 메서드를 사용할 수 있습니다.

```
/**
 * Get the user's featured posts.
 */
public function featuredPosts(): HasMany
{
    return $this->posts()->withAttributes(['featured' => true]);
}
```

<!-- The `withAttributes` method will add `where` clause constraints to the query using the given attributes, and it will also add the given attributes to any models created via the relationship method: -->
`withAttributes` 메서드는 주어진 속성을 기반으로 쿼리에 `where` 절을 추가하며, 해당 관계로 모델을 생성하는 경우에도 해당 속성을 자동으로 추가합니다.

```
$post = $user->featuredPosts()->create(['title' => 'Featured Post']);

$post->featured; // true
```

<a name="many-to-many"></a>
<!-- ## Many to Many Relationships -->
## Many to Many Relationships

<!-- Many-to-many relations are slightly more complicated than `hasOne` and `hasMany` relationships. An example of a many-to-many relationship is a user that has many roles and those roles are also shared by other users in the application. For example, a user may be assigned the role of "Author" and "Editor"; however, those roles may also be assigned to other users as well. So, a user has many roles and a role has many users. -->
다대다(many-to-many) 관계는 `hasOne`, `hasMany` 관계보다 구현이 약간 더 복잡합니다. 대표적인 예로, 하나의 사용자가 여러 역할을 가질 수 있고, 그 역할 역시 여러 사용자가 가질 수 있는 구조가 있습니다. 예를 들어 사용자 한 명이 "Author", "Editor" 역할을 가질 수 있으며, 이 역할들은 다른 사용자에게도 부여될 수 있습니다. 즉, 한 사용자는 여러 역할을 가질 수 있고, 하나의 역할 역시 여러 사용자와 연결됩니다.

<a name="many-to-many-table-structure"></a>
<!-- #### Table Structure -->
#### Table Structure

<!-- To define this relationship, three database tables are needed: `users`, `roles`, and `role_user`. The `role_user` table is derived from the alphabetical order of the related model names and contains `user_id` and `role_id` columns. This table is used as an intermediate table linking the users and roles. -->
이 관계를 정의하려면 `users`, `roles`, `role_user`라는 세 개의 테이블이 필요합니다. `role_user` 테이블은 서로 연관된 모델명의 알파벳 순서에 따라 이름이 정해지며, 이 테이블에는 `user_id`, `role_id` 컬럼이 존재합니다. 이 테이블은 사용자와 역할을 연결하는 중간 테이블로 기능합니다.

<!-- Remember, since a role can belong to many users, we cannot simply place a `user_id` column on the `roles` table. This would mean that a role could only belong to a single user. In order to provide support for roles being assigned to multiple users, the `role_user` table is needed. We can summarize the relationship's table structure like so: -->
여기서 주의할 점은, 하나의 역할이 여러 사용자에 속할 수 있으므로, 단순히 `roles` 테이블에 `user_id` 칼럼을 추가하는 방식으로 구현할 수 없다는 것입니다. 만약 그렇게 한다면 한 역할이 한 명의 사용자만 갖게 되는 구조가 되어버립니다. 여러 사용자에게 권한을 부여하려면 반드시 중간 테이블(`role_user`)이 필요합니다. 관계형 테이블 구조는 다음과 같이 요약할 수 있습니다.

```
users
    id - integer
    name - string

roles
    id - integer
    name - string

role_user
    user_id - integer
    role_id - integer
```

<a name="many-to-many-model-structure"></a>
<!-- #### Model Structure -->
#### Model Structure

<!-- Many-to-many relationships are defined by writing a method that returns the result of the `belongsToMany` method. The `belongsToMany` method is provided by the `Illuminate\Database\Eloquent\Model` base class that is used by all of your application's Eloquent models. For example, let's define a `roles` method on our `User` model. The first argument passed to this method is the name of the related model class: -->
다대다 관계는 `belongsToMany` 메서드에서 반환되는 결과를 리턴하는 메서드를 정의함으로써 설정할 수 있습니다. `belongsToMany` 메서드는 여러분의 모든 Eloquent 모델이 기본적으로 상속하는 `Illuminate\Database\Eloquent\Model` 클래스에서 제공됩니다. 예를 들어, `User` 모델에 `roles` 메서드를 다음과 같이 정의할 수 있습니다. 이 메서드의 첫 번째 인수로는 연관되는 모델 클래스명을 전달합니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class User extends Model
{
    /**
     * The roles that belong to the user.
     */
    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(Role::class);
    }
}
```

<!-- Once the relationship is defined, you may access the user's roles using the `roles` dynamic relationship property: -->
이렇게 관계를 정의하면, 사용자 객체의 동적 속성으로 `roles`를 통해 역할 목록에 접근할 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    // ...
}
```

<!-- Since all relationships also serve as query builders, you may add further constraints to the relationship query by calling the `roles` method and continuing to chain conditions onto the query: -->
모든 관계는 쿼리 빌더 역할도 하므로, `roles` 메서드를 호출한 후 체이닝으로 추가 조건을 붙여 쿼리를 세밀하게 제어할 수도 있습니다.

```
$roles = User::find(1)->roles()->orderBy('name')->get();
```

<!-- To determine the table name of the relationship's intermediate table, Eloquent will join the two related model names in alphabetical order. However, you are free to override this convention. You may do so by passing a second argument to the `belongsToMany` method: -->
중간 테이블의 이름은 Eloquent가 두 관련 모델의 이름을 알파벳 순서대로 결합하여 결정합니다. 하지만 이 규칙은 자유롭게 재정의할 수 있습니다. `belongsToMany` 메서드의 두 번째 인수로 직접 테이블 이름을 지정할 수 있습니다.

```
return $this->belongsToMany(Role::class, 'role_user');
```

<!-- In addition to customizing the name of the intermediate table, you may also customize the column names of the keys on the table by passing additional arguments to the `belongsToMany` method. The third argument is the foreign key name of the model on which you are defining the relationship, while the fourth argument is the foreign key name of the model that you are joining to: -->
또한, `belongsToMany` 메서드에 추가 인수를 전달해 중간 테이블의 외래 키 컬럼명도 직접 지정할 수 있습니다. 세 번째 인수는 현재 모델 기준의 외래 키, 네 번째 인수는 관계를 맺고자 하는 대상 모델의 외래 키입니다.

```
return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');
```

<a name="many-to-many-defining-the-inverse-of-the-relationship"></a>
<!-- #### Defining the Inverse of the Relationship -->
#### Defining the Inverse of the Relationship

<!-- To define the "inverse" of a many-to-many relationship, you should define a method on the related model which also returns the result of the `belongsToMany` method. To complete our user / role example, let's define the `users` method on the `Role` model: -->
다대다 관계의 "반대"도 역시 `belongsToMany` 메서드를 사용해 정의하면 됩니다. 예시를 완성해보면, `Role` 모델에 `users` 메서드를 정의할 수 있습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * The users that belong to the role.
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class);
    }
}
```

<!-- As you can see, the relationship is defined exactly the same as its `User` model counterpart with the exception of referencing the `App\Models\User` model. Since we're reusing the `belongsToMany` method, all of the usual table and key customization options are available when defining the "inverse" of many-to-many relationships. -->
보시는 것처럼, 관계 정의 방식은 `User` 모델에서와 동일하며, 단지 참조되는 모델만 `App\Models\User`로 바뀌는 점이 다릅니다. `belongsToMany` 메서드를 재사용하기 때문에, 테이블명이나 키 컬럼명 커스터마이징 역시 언제든 동일하게 적용할 수 있습니다.

<a name="retrieving-intermediate-table-columns"></a>
<!-- ### Retrieving Intermediate Table Columns -->
### Retrieving Intermediate Table Columns

<!-- As you have already learned, working with many-to-many relations requires the presence of an intermediate table. Eloquent provides some very helpful ways of interacting with this table. For example, let's assume our `User` model has many `Role` models that it is related to. After accessing this relationship, we may access the intermediate table using the `pivot` attribute on the models: -->
이미 살펴본 것처럼, 다대다 관계를 사용할 때는 중간 테이블이 반드시 필요합니다. Eloquent는 이 중간 테이블과 상호작용할 수 있는 다양한 유용한 기능을 제공합니다. 예를 들어, `User` 모델이 여러 `Role` 모델과 연결되어 있다면, 역할을 조회한 후 각 모델의 `pivot` 속성을 이용해 중간 테이블 데이터에 접근할 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    echo $role->pivot->created_at;
}
```

<!-- Notice that each `Role` model we retrieve is automatically assigned a `pivot` attribute. This attribute contains a model representing the intermediate table. -->
이 예제처럼, 조회한 각각의 `Role` 모델에는 자동으로 `pivot` 속성이 부여됩니다. 이 속성은 중간 테이블(피벗 테이블)의 데이터를 담고 있는 모델입니다.

<!-- By default, only the model keys will be present on the `pivot` model. If your intermediate table contains extra attributes, you must specify them when defining the relationship: -->
기본적으로는 모델 키 정보만 `pivot` 모델에 포함됩니다. 만약 중간 테이블에 추가적인 속성이 있다면, 관계를 정의할 때 그 속성들을 명시해주어야 합니다.

```
return $this->belongsToMany(Role::class)->withPivot('active', 'created_by');
```

<!-- If you would like your intermediate table to have `created_at` and `updated_at` timestamps that are automatically maintained by Eloquent, call the `withTimestamps` method when defining the relationship: -->
또한 중간 테이블에 `created_at`, `updated_at` 타임스탬프가 있고 이를 Eloquent에서 자동 관리하고 싶다면, 관계에 `withTimestamps` 메서드를 추가하세요.

```
return $this->belongsToMany(Role::class)->withTimestamps();
```

> [!WARNING]
> Eloquent에서 자동으로 타임스탬프를 관리하는 중간 테이블은 `created_at`, `updated_at` 컬럼을 반드시 포함해야 합니다.

<a name="customizing-the-pivot-attribute-name"></a>
<!-- #### Customizing the `pivot` Attribute Name -->
#### Customizing the `pivot` Attribute Name

<!-- As noted previously, attributes from the intermediate table may be accessed on models via the `pivot` attribute. However, you are free to customize the name of this attribute to better reflect its purpose within your application. -->
앞서 설명했듯이, 중간 테이블의 속성은 모델의 `pivot` 속성을 통해 접근할 수 있습니다. 하지만, 필요에 따라 이 속성명을 여러분의 애플리케이션 상황에 맞게 변경하는 것도 가능합니다.

<!-- For example, if your application contains users that may subscribe to podcasts, you likely have a many-to-many relationship between users and podcasts. If this is the case, you may wish to rename your intermediate table attribute to `subscription` instead of `pivot`. This can be done using the `as` method when defining the relationship: -->
예를 들어, 사용자가 팟캐스트를 구독하는 경우가 있을 때, users와 podcasts 간의 다대다 관계를 가지게 되는데, 이때 중간 테이블 속성명을 `pivot` 대신 `subscription`으로 바꾸고 싶을 수 있습니다. 관계 정의 때 `as` 메서드를 사용하면 됩니다.

```
return $this->belongsToMany(Podcast::class)
    ->as('subscription')
    ->withTimestamps();
```

<!-- Once the custom intermediate table attribute has been specified, you may access the intermediate table data using the customized name: -->
이렇게 커스텀 속성명을 지정했다면, 관계 데이터를 해당 이름으로 접근할 수 있습니다.

```
$users = User::with('podcasts')->get();

foreach ($users->flatMap->podcasts as $podcast) {
    echo $podcast->subscription->created_at;
}
```

<a name="filtering-queries-via-intermediate-table-columns"></a>
<!-- ### Filtering Queries via Intermediate Table Columns -->
### Filtering Queries via Intermediate Table Columns

<!-- You can also filter the results returned by `belongsToMany` relationship queries using the `wherePivot`, `wherePivotIn`, `wherePivotNotIn`, `wherePivotBetween`, `wherePivotNotBetween`, `wherePivotNull`, and `wherePivotNotNull` methods when defining the relationship: -->
`belongsToMany` 관계 쿼리에서는 중간 테이블 컬럼을 기준으로 결과를 필터링할 수 있습니다. 이를 위해 `wherePivot`, `wherePivotIn`, `wherePivotNotIn`, `wherePivotBetween`, `wherePivotNotBetween`, `wherePivotNull`, `wherePivotNotNull` 등의 메서드를 사용할 수 있습니다.

```
return $this->belongsToMany(Role::class)
    ->wherePivot('approved', 1);

return $this->belongsToMany(Role::class)
    ->wherePivotIn('priority', [1, 2]);

return $this->belongsToMany(Role::class)
    ->wherePivotNotIn('priority', [1, 2]);

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotBetween('created_at', ['2020-01-01 00:00:00', '2020-12-31 00:00:00']);

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotNotBetween('created_at', ['2020-01-01 00:00:00', '2020-12-31 00:00:00']);

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotNull('expired_at');

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotNotNull('expired_at');
```

<!-- The `wherePivot` adds a where clause constraint to the query, but does not add the specified value when creating new models via the defined relationship. If you need to both query and create relationships with a particular pivot value, you may use the `withPivotValue` method: -->
`wherePivot`은 쿼리에 where 조건을 추가해주지만, 관계를 통해 새 모델을 생성할 때 지정된 값을 자동으로 추가하지는 않습니다. 쿼리와 생성 모두에 같은 pivot 값을 적용하고 싶다면 `withPivotValue` 메서드를 사용할 수 있습니다.

```
return $this->belongsToMany(Role::class)
        ->withPivotValue('approved', 1);
```

<a name="ordering-queries-via-intermediate-table-columns"></a>
<!-- ### Ordering Queries via Intermediate Table Columns -->
### Ordering Queries via Intermediate Table Columns

<!-- You can order the results returned by `belongsToMany` relationship queries using the `orderByPivot` method. In the following example, we will retrieve all of the latest badges for the user: -->
`belongsToMany` 관계 쿼리에서 `orderByPivot` 메서드를 사용해 중간 테이블 컬럼을 기준으로 결과를 정렬할 수 있습니다. 다음 예제는 사용자의 뱃지 중 최신 뱃지를 조회하는 방법을 보여줍니다.

```
return $this->belongsToMany(Badge::class)
    ->where('rank', 'gold')
    ->orderByPivot('created_at', 'desc');
```

<a name="defining-custom-intermediate-table-models"></a>
<!-- ### Defining Custom Intermediate Table Models -->
### Defining Custom Intermediate Table Models

<!-- If you would like to define a custom model to represent the intermediate table of your many-to-many relationship, you may call the `using` method when defining the relationship. Custom pivot models give you the opportunity to define additional behavior on the pivot model, such as methods and casts. -->
다대다 관계의 중간 테이블을 대표하는 커스텀 모델을 별도로 정의하고 싶다면, 관계 정의 시 `using` 메서드를 통해 피벗 모델을 지정할 수 있습니다. 커스텀 피벗 모델을 사용하면, 특정 메서드나 값 변환(cast) 등 부가적인 동작을 추가로 정의할 수 있습니다.

<!-- Custom many-to-many pivot models should extend the `Illuminate\Database\Eloquent\Relations\Pivot` class while custom polymorphic many-to-many pivot models should extend the `Illuminate\Database\Eloquent\Relations\MorphPivot` class. For example, we may define a `Role` model which uses a custom `RoleUser` pivot model: -->
커스텀 다대다 피벗 모델은 `Illuminate\Database\Eloquent\Relations\Pivot` 클래스를 반드시 상속해야 하며, 다형성 다대다 피벗 모델은 `Illuminate\Database\Eloquent\Relations\MorphPivot`을 상속해야 합니다. 예시로, `Role` 모델이 `RoleUser`라는 커스텀 피벗 모델을 사용하는 경우를 살펴봅시다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * The users that belong to the role.
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class)->using(RoleUser::class);
    }
}
```

<!-- When defining the `RoleUser` model, you should extend the `Illuminate\Database\Eloquent\Relations\Pivot` class: -->
이제 `RoleUser` 모델을 정의할 때는 `Illuminate\Database\Eloquent\Relations\Pivot` 클래스를 상속해야 합니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Relations\Pivot;

class RoleUser extends Pivot
{
    // ...
}
```

> [!WARNING]
> 피벗(pivot) 모델에서는 `SoftDeletes` 트레이트를 사용할 수 없습니다. 피벗 레코드에 소프트 딜리트 기능이 필요한 경우, 해당 피벗 모델을 실제 Eloquent 모델로 전환하는 것을 고려하세요.

<a name="custom-pivot-models-and-incrementing-ids"></a>
<!-- #### Custom Pivot Models and Incrementing IDs -->
#### Custom Pivot Models and Incrementing IDs

<!-- If you have defined a many-to-many relationship that uses a custom pivot model, and that pivot model has an auto-incrementing primary key, you should ensure your custom pivot model class defines an `incrementing` property that is set to `true`. -->
만약 자동 증가되는(primary key가 auto-increment) 기본키를 가진 커스텀 피벗 모델을 정의한다면, 반드시 해당 피벗 모델 클래스에 `incrementing` 속성을 `true`로 명시해야 합니다.

```
/**
 * Indicates if the IDs are auto-incrementing.
 *
 * @var bool
 */
public $incrementing = true;
```

<a name="polymorphic-relationships"></a>
<!-- ## Polymorphic Relationships -->
## Polymorphic Relationships

<!-- A polymorphic relationship allows the child model to belong to more than one type of model using a single association. For example, imagine you are building an application that allows users to share blog posts and videos. In such an application, a `Comment` model might belong to both the `Post` and `Video` models. -->
다형성(polymorphic) 관계를 사용하면, 하나의 자식 모델이 단일 연관 컬럼을 통해 여러 타입의 부모 모델과 연결될 수 있습니다. 예를 들어, 블로그 게시글과 동영상을 공유할 수 있는 애플리케이션을 만든다고 가정하면, `Comment` 모델은 `Post` 모델과 `Video` 모델 모두와 연관될 수 있습니다.

<a name="one-to-one-polymorphic-relations"></a>
<!-- ### One to One (Polymorphic) -->
### One to One (Polymorphic)

<a name="one-to-one-polymorphic-table-structure"></a>
<!-- #### Table Structure -->
#### Table Structure

<!-- A one-to-one polymorphic relation is similar to a typical one-to-one relation; however, the child model can belong to more than one type of model using a single association. For example, a blog `Post` and a `User` may share a polymorphic relation to an `Image` model. Using a one-to-one polymorphic relation allows you to have a single table of unique images that may be associated with posts and users. First, let's examine the table structure: -->
일대일 다형성 관계는 일반적인 일대일(one-to-one) 관계와 유사하지만, 자식 모델이 단일 연관 컬럼을 사용해 여러 타입의 부모 모델과 연관될 수 있다는 점이 다릅니다. 예를 들어, 블로그의 `Post`와 `User`는 공통적으로 `Image` 모델과 다형성 관계를 가질 수 있습니다. 이를 통해 하나의 이미지 테이블을 두고, 게시글이나 유저 모두 특정 이미지에 연결 가능한 구조가 됩니다. 테이블 구조는 다음과 같습니다.

```
posts
    id - integer
    name - string

users
    id - integer
    name - string

images
    id - integer
    url - string
    imageable_id - integer
    imageable_type - string
```

<!-- Note the `imageable_id` and `imageable_type` columns on the `images` table. The `imageable_id` column will contain the ID value of the post or user, while the `imageable_type` column will contain the class name of the parent model. The `imageable_type` column is used by Eloquent to determine which "type" of parent model to return when accessing the `imageable` relation. In this case, the column would contain either `App\Models\Post` or `App\Models\User`. -->
여기서 `images` 테이블의 `imageable_id`, `imageable_type` 컬럼에 주목하세요. `imageable_id` 컬럼은 게시글 혹은 사용자의 ID 값을 저장하고, `imageable_type` 컬럼은 부모 모델의 클래스명을 저장합니다. Eloquent는 `imageable` 연관관계에 접근할 때 이 `imageable_type`을 이용해 어떤 유형의 부모 모델을 가져와야 하는지 결정하며, 예를 들어 이 값이 `App\Models\Post` 또는 `App\Models\User`가 될 수 있습니다.

<a name="one-to-one-polymorphic-model-structure"></a>
<!-- #### Model Structure -->
#### Model Structure

<!-- Next, let's examine the model definitions needed to build this relationship: -->
이제 이 관계를 구현하기 위해 어떤 모델 정의가 필요한지 살펴봅니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Image extends Model
{
    /**
     * Get the parent imageable model (user or post).
     */
    public function imageable(): MorphTo
    {
        return $this->morphTo();
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphOne;

class Post extends Model
{
    /**
     * Get the post's image.
     */
    public function image(): MorphOne
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphOne;

class User extends Model
{
    /**
     * Get the user's image.
     */
    public function image(): MorphOne
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}
```

<a name="one-to-one-polymorphic-retrieving-the-relationship"></a>
<!-- #### Retrieving the Relationship -->
#### Retrieving the Relationship

<!-- Once your database table and models are defined, you may access the relationships via your models. For example, to retrieve the image for a post, we can access the `image` dynamic relationship property: -->
데이터베이스 테이블과 모델이 준비되었다면, 이제 각 모델의 동적 관계 속성을 활용해 연관 데이터를 조회할 수 있습니다. 예를 들어, 게시글의 이미지를 가져오려면 `image` 동적 연관관계 속성으로 접근합니다.

```
use App\Models\Post;

$post = Post::find(1);

$image = $post->image;
```

<!-- You may retrieve the parent of the polymorphic model by accessing the name of the method that performs the call to `morphTo`. In this case, that is the `imageable` method on the `Image` model. So, we will access that method as a dynamic relationship property: -->
반대로 다형성 모델의 부모 모델을 조회하려면, `morphTo`를 호출하는 메서드의 이름(여기선 `Image` 모델의 `imageable` 메서드)을 동적 속성처럼 사용하면 됩니다.

```
use App\Models\Image;

$image = Image::find(1);

$imageable = $image->imageable;
```

<!-- The `imageable` relation on the `Image` model will return either a `Post` or `User` instance, depending on which type of model owns the image. -->
`Image` 모델의 `imageable` 관계는 해당 이미지를 소유한 `Post` 또는 `User` 중 하나의 인스턴스를 반환합니다.

<a name="morph-one-to-one-key-conventions"></a>
<!-- #### Key Conventions -->
#### Key Conventions

<!-- If necessary, you may specify the name of the "id" and "type" columns utilized by your polymorphic child model. If you do so, ensure that you always pass the name of the relationship as the first argument to the `morphTo` method. Typically, this value should match the method name, so you may use PHP's `__FUNCTION__` constant: -->
필요하다면, 다형성 자식 모델에 사용되는 "id" 및 "type" 컬럼의 이름을 직접 지정할 수도 있습니다. 이 경우 반드시 관계 메서드 이름을 첫 인수로 `morphTo`에 전달해야 하며, 일반적으로는 메서드명과 일치시키기 위해 PHP의 `__FUNCTION__` 상수를 사용할 수 있습니다.

```
/**
 * Get the model that the image belongs to.
 */
public function imageable(): MorphTo
{
    return $this->morphTo(__FUNCTION__, 'imageable_type', 'imageable_id');
}
```

<a name="one-to-many-polymorphic-relations"></a>
<!-- ### One to Many (Polymorphic) -->
### One to Many (Polymorphic)

<a name="one-to-many-polymorphic-table-structure"></a>
<!-- #### Table Structure -->
#### Table Structure

<!-- A one-to-many polymorphic relation is similar to a typical one-to-many relation; however, the child model can belong to more than one type of model using a single association. For example, imagine users of your application can "comment" on posts and videos. Using polymorphic relationships, you may use a single `comments` table to contain comments for both posts and videos. First, let's examine the table structure required to build this relationship: -->
일대다 다형성 관계 역시 일반적인 일대다 관계와 유사하지만, 자식 모델이 단일 연관 컬럼을 통해 여러 타입의 부모 모델과 연결될 수 있다는 점이 다릅니다. 예를 들어, 여러분의 애플리케이션에서 사용자가 게시글과 동영상 모두에 "댓글(comment)"을 남길 수 있다고 가정해봅시다. 다형성 관계를 사용하면, 단 하나의 `comments` 테이블이 게시글과 동영상을 모두 참조하는 구조를 만들 수 있습니다. 요구되는 테이블 구조는 다음과 같습니다.

```
posts
    id - integer
    title - string
    body - text

videos
    id - integer
    title - string
    url - string

comments
    id - integer
    body - text
    commentable_id - integer
    commentable_type - string
```

<a name="one-to-many-polymorphic-model-structure"></a>

<!-- #### Model Structure -->
#### Model Structure

<!-- Next, let's examine the model definitions needed to build this relationship: -->
다음으로, 이 관계를 구축하는 데 필요한 모델 정의를 살펴보겠습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Comment extends Model
{
    /**
     * Get the parent commentable model (post or video).
     */
    public function commentable(): MorphTo
    {
        return $this->morphTo();
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphMany;

class Post extends Model
{
    /**
     * Get all of the post's comments.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphMany;

class Video extends Model
{
    /**
     * Get all of the video's comments.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}
```

<a name="one-to-many-polymorphic-retrieving-the-relationship"></a>
<!-- #### Retrieving the Relationship -->
#### Retrieving the Relationship

<!-- Once your database table and models are defined, you may access the relationships via your model's dynamic relationship properties. For example, to access all of the comments for a post, we can use the `comments` dynamic property: -->
데이터베이스 테이블과 모델이 정의되면, 모델의 동적 관계 속성을 통해 관계를 조회할 수 있습니다. 예를 들어, 특정 포스트의 모든 댓글을 조회하고 싶다면 `comments` 동적 속성을 사용할 수 있습니다.

```
use App\Models\Post;

$post = Post::find(1);

foreach ($post->comments as $comment) {
    // ...
}
```

<!-- You may also retrieve the parent of a polymorphic child model by accessing the name of the method that performs the call to `morphTo`. In this case, that is the `commentable` method on the `Comment` model. So, we will access that method as a dynamic relationship property in order to access the comment's parent model: -->
다형적(child) 모델에서 부모 모델을 조회할 때는 `morphTo`를 호출하는 메서드명을 동적 속성으로 조회하면 됩니다. 이 예시의 경우 `Comment` 모델의 `commentable` 메서드가 해당합니다. 즉, 이 메서드를 동적 관계 속성으로 접근함으로써 댓글의 부모 모델을 얻을 수 있습니다.

```
use App\Models\Comment;

$comment = Comment::find(1);

$commentable = $comment->commentable;
```

<!-- The `commentable` relation on the `Comment` model will return either a `Post` or `Video` instance, depending on which type of model is the comment's parent. -->
`Comment` 모델의 `commentable` 관계는, 어떤 타입의 모델이 부모인지에 따라 `Post` 인스턴스 또는 `Video` 인스턴스를 반환하게 됩니다.

<a name="polymorphic-automatically-hydrating-parent-models-on-children"></a>
<!-- #### Automatically Hydrating Parent Models on Children -->
#### Automatically Hydrating Parent Models on Children

<!-- Even when utilizing Eloquent eager loading, "N + 1" query problems can arise if you try to access the parent model from a child model while looping through the child models: -->
Eloquent의 eager loading을 사용하더라도, 자식 모델에서 부모 모델을 반복문 내에서 접근하면 "N + 1" 쿼리 문제가 발생할 수 있습니다.

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->commentable->title;
    }
}
```

<!-- In the example above, an "N + 1" query problem has been introduced because, even though comments were eager loaded for every `Post` model, Eloquent does not automatically hydrate the parent `Post` on each child `Comment` model. -->
위 예시에서는 모든 `Post` 모델에 대해 댓글이 eager load되었음에도 불구하고, 자식 `Comment` 모델에서는 부모 `Post`가 자동으로 hydrate되지 않기 때문에 "N + 1" 쿼리 문제가 발생합니다.

<!-- If you would like Eloquent to automatically hydrate parent models onto their children, you may invoke the `chaperone` method when defining a `morphMany` relationship: -->
Eloquent가 부모 모델을 자식에게 자동으로 hydrate(연결)하도록 하고 싶다면, `morphMany` 관계를 정의할 때 `chaperone` 메서드를 호출하면 됩니다.

```
class Post extends Model
{
    /**
     * Get all of the post's comments.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable')->chaperone();
    }
}
```

<!-- Or, if you would like to opt-in to automatic parent hydration at run time, you may invoke the `chaperone` model when eager loading the relationship: -->
또는 런타임에 자동 부모 바인딩을 직접 opt-in 하고 싶다면, 관계를 eager load할 때 `chaperone` 메서드를 사용할 수 있습니다.

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-of-many-polymorphic-relations"></a>
<!-- ### One of Many (Polymorphic) -->
### One of Many (Polymorphic)

<!-- Sometimes a model may have many related models, yet you want to easily retrieve the "latest" or "oldest" related model of the relationship. For example, a `User` model may be related to many `Image` models, but you want to define a convenient way to interact with the most recent image the user has uploaded. You may accomplish this using the `morphOne` relationship type combined with the `ofMany` methods: -->
하나의 모델이 여러 관련 모델을 가질 수 있지만, 그 중 "가장 최신" 혹은 "가장 오래된" 모델을 쉽게 조회하고 싶을 때가 있습니다. 예를 들어 `User` 모델이 여러 `Image` 모델과 관계를 맺고 있지만, 사용자가 마지막으로 업로드한 이미지를 편리하게 조회하고 싶을 수 있습니다. 이런 경우 `morphOne` 관계 타입과 `ofMany` 메서드를 조합하여 사용할 수 있습니다.

```php
/**
 * Get the user's most recent image.
 */
public function latestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->latestOfMany();
}
```

<!-- Likewise, you may define a method to retrieve the "oldest", or first, related model of a relationship: -->
이와 비슷하게, "가장 오래된" 혹은 첫 번째 관련 모델을 조회하는 메서드를 정의할 수도 있습니다.

```php
/**
 * Get the user's oldest image.
 */
public function oldestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->oldestOfMany();
}
```

<!-- By default, the `latestOfMany` and `oldestOfMany` methods will retrieve the latest or oldest related model based on the model's primary key, which must be sortable. However, sometimes you may wish to retrieve a single model from a larger relationship using a different sorting criteria. -->
기본적으로, `latestOfMany`와 `oldestOfMany` 메서드는 모델의 기본 키(primary key, 정렬 가능한 값)를 기준으로 최신 혹은 오래된 관련 모델을 가져옵니다. 하지만, 더 다양한 정렬 기준으로 단일 모델을 조회하고 싶을 때도 있습니다.

<!-- For example, using the `ofMany` method, you may retrieve the user's most "liked" image. The `ofMany` method accepts the sortable column as its first argument and which aggregate function (`min` or `max`) to apply when querying for the related model: -->
예를 들어, `ofMany` 메서드를 사용하면 사용자의 "좋아요"가 가장 많은 이미지를 가져올 수 있습니다. `ofMany` 메서드는 첫 번째 인수로 정렬할 컬럼명을, 두 번째 인수로 집계 함수(`min` 또는 `max`)를 받습니다.

```php
/**
 * Get the user's most popular image.
 */
public function bestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->ofMany('likes', 'max');
}
```

> [!NOTE]
> 보다 고급스러운 "one of many" 관계도 구성할 수 있습니다. 자세한 내용은 [has one of many documentation](#advanced-has-one-of-many-relationships)를 참고하시기 바랍니다.

<a name="many-to-many-polymorphic-relations"></a>
<!-- ### Many to Many (Polymorphic) -->
### Many to Many (Polymorphic)

<a name="many-to-many-polymorphic-table-structure"></a>
<!-- #### Table Structure -->
#### Table Structure

<!-- Many-to-many polymorphic relations are slightly more complicated than "morph one" and "morph many" relationships. For example, a `Post` model and `Video` model could share a polymorphic relation to a `Tag` model. Using a many-to-many polymorphic relation in this situation would allow your application to have a single table of unique tags that may be associated with posts or videos. First, let's examine the table structure required to build this relationship: -->
다대다(polymorphic) 관계는 "morph one"이나 "morph many" 관계보다 약간 더 복잡합니다. 예를 들어, `Post` 모델과 `Video` 모델이 공통의 다형적 관계를 통해 `Tag` 모델과 연결될 수 있습니다. 이렇게 하면, 포스트나 비디오에 공통적으로 태그를 단일 테이블에 저장하여 재활용할 수 있습니다. 먼저, 이 관계를 구성하기 위한 테이블 구조를 살펴보겠습니다.

```
posts
    id - integer
    name - string

videos
    id - integer
    name - string

tags
    id - integer
    name - string

taggables
    tag_id - integer
    taggable_id - integer
    taggable_type - string
```

> [!NOTE]
> 다형 다대다 관계를 본격적으로 다루기 전에 일반적인 [many-to-many relationships](#many-to-many)에 대한 문서를 읽어보시면 도움이 됩니다.

<a name="many-to-many-polymorphic-model-structure"></a>
<!-- #### Model Structure -->
#### Model Structure

<!-- Next, we're ready to define the relationships on the models. The `Post` and `Video` models will both contain a `tags` method that calls the `morphToMany` method provided by the base Eloquent model class. -->
다음으로, 각 모델에 관계를 정의합니다. `Post`와 `Video` 모델 모두 Eloquent 기반 클래스가 제공하는 `morphToMany` 메서드를 사용하는 `tags` 메서드를 포함하게 됩니다.

<!-- The `morphToMany` method accepts the name of the related model as well as the "relationship name". Based on the name we assigned to our intermediate table name and the keys it contains, we will refer to the relationship as "taggable": -->
`morphToMany` 메서드는 관계맺을 모델명과 "관계 이름"을 인수로 받습니다. 중간 테이블명과 포함된 키명에 따라 관계 이름은 "taggable"로 지정합니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Post extends Model
{
    /**
     * Get all of the tags for the post.
     */
    public function tags(): MorphToMany
    {
        return $this->morphToMany(Tag::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-defining-the-inverse-of-the-relationship"></a>
<!-- #### Defining the Inverse of the Relationship -->
#### Defining the Inverse of the Relationship

<!-- Next, on the `Tag` model, you should define a method for each of its possible parent models. So, in this example, we will define a `posts` method and a `videos` method. Both of these methods should return the result of the `morphedByMany` method. -->
이번에는 `Tag` 모델에서 각각의 부모 모델에 대해 메서드를 정의해야 합니다. 이 예시에서는 `posts` 메서드와 `videos` 메서드를 정의하게 되며, 두 메서드 모두 `morphedByMany` 메서드를 반환해야 합니다.

<!-- The `morphedByMany` method accepts the name of the related model as well as the "relationship name". Based on the name we assigned to our intermediate table name and the keys it contains, we will refer to the relationship as "taggable": -->
`morphedByMany` 메서드는 관계맺을 모델명과 "관계 이름"을 인수로 받습니다. 관계명은 "taggable"로 지정합니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Tag extends Model
{
    /**
     * Get all of the posts that are assigned this tag.
     */
    public function posts(): MorphToMany
    {
        return $this->morphedByMany(Post::class, 'taggable');
    }

    /**
     * Get all of the videos that are assigned this tag.
     */
    public function videos(): MorphToMany
    {
        return $this->morphedByMany(Video::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-retrieving-the-relationship"></a>
<!-- #### Retrieving the Relationship -->
#### Retrieving the Relationship

<!-- Once your database table and models are defined, you may access the relationships via your models. For example, to access all of the tags for a post, you may use the `tags` dynamic relationship property: -->
데이터베이스 테이블과 모델이 정의되면, 모델을 통해 관계를 조회할 수 있습니다. 예를 들어, 포스트의 모든 태그를 가져오고 싶다면 `tags` 동적 속성을 사용할 수 있습니다.

```
use App\Models\Post;

$post = Post::find(1);

foreach ($post->tags as $tag) {
    // ...
}
```

<!-- You may retrieve the parent of a polymorphic relation from the polymorphic child model by accessing the name of the method that performs the call to `morphedByMany`. In this case, that is the `posts` or `videos` methods on the `Tag` model: -->
다형적 관계의 자식 모델에서 부모 모델을 조회할 때는 `morphedByMany`를 호출하는 메서드명을 이용합니다. 이번 예시에서는 `Tag` 모델의 `posts` 또는 `videos` 메서드가 해당합니다.

```
use App\Models\Tag;

$tag = Tag::find(1);

foreach ($tag->posts as $post) {
    // ...
}

foreach ($tag->videos as $video) {
    // ...
}
```

<a name="custom-polymorphic-types"></a>
<!-- ### Custom Polymorphic Types -->
### Custom Polymorphic Types

<!-- By default, Laravel will use the fully qualified class name to store the "type" of the related model. For instance, given the one-to-many relationship example above where a `Comment` model may belong to a `Post` or a `Video` model, the default `commentable_type` would be either `App\Models\Post` or `App\Models\Video`, respectively. However, you may wish to decouple these values from your application's internal structure. -->
Laravel에서 "타입" 정보를 저장할 때는 기본적으로 완전히 네임스페이스가 적용된 클래스명을 사용합니다. 예를 들어, 앞서 다룬 일대다 관계 예시에서 `Comment` 모델이 `Post` 또는 `Video`에 속해 있을 경우, 기본적으로 `commentable_type` 컬럼에는 각각 `App\Models\Post` 또는 `App\Models\Video`가 저장됩니다. 하지만 모델명과 내부 구조를 분리하고 싶을 때도 있습니다.

<!-- For example, instead of using the model names as the "type", we may use simple strings such as `post` and `video`. By doing so, the polymorphic "type" column values in our database will remain valid even if the models are renamed: -->
예를 들어, 타입 정보로 모델명이 아닌 간단한 문자열(`post`, `video`)을 사용할 수 있습니다. 이렇게 하면, 모델명을 변경해도 데이터베이스의 다형 타입 컬럼 값이 유효하게 유지됩니다.

```
use Illuminate\Database\Eloquent\Relations\Relation;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);
```

<!-- You may call the `enforceMorphMap` method in the `boot` method of your `App\Providers\AppServiceProvider` class or create a separate service provider if you wish. -->
`enforceMorphMap` 메서드는 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출하거나, 필요하다면 별도의 서비스 프로바이더에서 호출할 수도 있습니다.

<!-- You may determine the morph alias of a given model at runtime using the model's `getMorphClass` method. Conversely, you may determine the fully-qualified class name associated with a morph alias using the `Relation::getMorphedModel` method: -->
런타임에 모델별로 morph alias를 알아내고 싶다면 모델의 `getMorphClass` 메서드를 사용할 수 있습니다. 반대로, morph alias로부터 완전한 클래스명을 얻으려면 `Relation::getMorphedModel` 메서드를 이용할 수 있습니다.

```
use Illuminate\Database\Eloquent\Relations\Relation;

$alias = $post->getMorphClass();

$class = Relation::getMorphedModel($alias);
```

> [!WARNING]
> 기존 애플리케이션에 "morph map"을 추가할 경우, 데이터베이스 내 morphable `*_type` 컬럼 값 중 클래스명을 포함하는 값들은 반드시 "맵"에 사용된 이름으로 변환해주어야 합니다.

<a name="dynamic-relationships"></a>
<!-- ### Dynamic Relationships -->
### Dynamic Relationships

<!-- You may use the `resolveRelationUsing` method to define relations between Eloquent models at runtime. While not typically recommended for normal application development, this may occasionally be useful when developing Laravel packages. -->
`resolveRelationUsing` 메서드를 사용하면 Eloquent 모델 간의 관계를 런타임 시점에 정의할 수 있습니다. 일반적인 애플리케이션 개발에서는 자주 사용하지 않지만, Laravel 패키지 개발 시에는 유용할 수 있습니다.

<!-- The `resolveRelationUsing` method accepts the desired relationship name as its first argument. The second argument passed to the method should be a closure that accepts the model instance and returns a valid Eloquent relationship definition. Typically, you should configure dynamic relationships within the boot method of a [service provider](/docs/11.x/providers): -->
`resolveRelationUsing` 메서드는 첫 번째 인수로 관계명을, 두 번째 인수로 모델 인스턴스를 받아 유효한 Eloquent 관계를 반환하는 클로저를 받습니다. 보통 동적 관계는 [service provider](/docs/11.x/providers)의 boot 메서드에서 설정합니다.

```
use App\Models\Order;
use App\Models\Customer;

Order::resolveRelationUsing('customer', function (Order $orderModel) {
    return $orderModel->belongsTo(Customer::class, 'customer_id');
});
```

> [!WARNING]
> 동적 관계를 정의할 때는 항상 Eloquent 관계 메서드에 명시적으로 키 이름을 전달해 주어야 합니다.

<a name="querying-relations"></a>
<!-- ## Querying Relations -->
## Querying Relations

<!-- Since all Eloquent relationships are defined via methods, you may call those methods to obtain an instance of the relationship without actually executing a query to load the related models. In addition, all types of Eloquent relationships also serve as [query builders](/docs/11.x/queries), allowing you to continue to chain constraints onto the relationship query before finally executing the SQL query against your database. -->
모든 Eloquent 관계는 메서드 형태로 정의되어 있기 때문에, 실제 쿼리를 실행하지 않고도 해당 관계 인스턴스를 얻을 수 있습니다. 또한 모든 Eloquent 관계는 [query builders](/docs/11.x/queries)의 역할도 하며, 관계 쿼리에 다양한 제약 조건을 체이닝한 후 최종적으로 SQL 쿼리를 실행할 수 있습니다.

<!-- For example, imagine a blog application in which a `User` model has many associated `Post` models: -->
예를 들어, 블로그 애플리케이션에서 `User` 모델이 여러 `Post` 모델과 관계를 가진다고 가정해봅니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * Get all of the posts for the user.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }
}
```

<!-- You may query the `posts` relationship and add additional constraints to the relationship like so: -->
`posts` 관계에 쿼리 조건을 추가하려면 아래와 같이 하면 됩니다.

```
use App\Models\User;

$user = User::find(1);

$user->posts()->where('active', 1)->get();
```

<!-- You are able to use any of the Laravel [query builder's](/docs/11.x/queries) methods on the relationship, so be sure to explore the query builder documentation to learn about all of the methods that are available to you. -->
모든 Laravel [query builder's](/docs/11.x/queries) 메서드는 관계 쿼리에도 사용할 수 있으므로, 쿼리 빌더 문서를 참고해 다양한 메서드를 활용하시기 바랍니다.

<a name="chaining-orwhere-clauses-after-relationships"></a>
<!-- #### Chaining `orWhere` Clauses After Relationships -->
#### Chaining `orWhere` Clauses After Relationships

<!-- As demonstrated in the example above, you are free to add additional constraints to relationships when querying them. However, use caution when chaining `orWhere` clauses onto a relationship, as the `orWhere` clauses will be logically grouped at the same level as the relationship constraint: -->
위 예시처럼 관계 쿼리에 추가로 제약 조건을 붙일 수 있지만, `orWhere` 절을 체이닝할 때는 주의가 필요합니다. `orWhere` 절은 관계 제약과 논리적으로 동일 레벨에서 그룹화되기 때문입니다.

```
$user->posts()
        ->where('active', 1)
        ->orWhere('votes', '>=', 100)
        ->get();
```

<!-- The example above will generate the following SQL. As you can see, the `or` clause instructs the query to return _any_ post with greater than 100 votes. The query is no longer constrained to a specific user: -->
위 예시는 다음과 같은 SQL을 생성합니다. `or` 절에 의해 100표 이상인 모든 포스트가 반환되므로, 쿼리가 특정 사용자에 한정되지 않게 됩니다.

```sql
select *
from posts
where user_id = ? and active = 1 or votes >= 100
```

<!-- In most situations, you should use [logical groups](/docs/11.x/queries#logical-grouping) to group the conditional checks between parentheses: -->
대부분의 상황에서는 [logical groups](/docs/11.x/queries#logical-grouping)을 사용하여 조건을 괄호로 묶어주어야 합니다.

```
use Illuminate\Database\Eloquent\Builder;

$user->posts()
    ->where(function (Builder $query) {
        return $query->where('active', 1)
            ->orWhere('votes', '>=', 100);
    })
    ->get();
```

<!-- The example above will produce the following SQL. Note that the logical grouping has properly grouped the constraints and the query remains constrained to a specific user: -->
위 방식에서는 다음과 같은 SQL이 생성되어, 논리 그룹이 올바르게 처리되고 쿼리 결과가 특정 사용자에 한정됩니다.

```sql
select *
from posts
where user_id = ? and (active = 1 or votes >= 100)
```

<a name="relationship-methods-vs-dynamic-properties"></a>
<!-- ### Relationship Methods vs. Dynamic Properties -->
### Relationship Methods vs. Dynamic Properties

<!-- If you do not need to add additional constraints to an Eloquent relationship query, you may access the relationship as if it were a property. For example, continuing to use our `User` and `Post` example models, we may access all of a user's posts like so: -->
Eloquent 관계 쿼리에 추가 제약 조건을 줄 필요가 없다면, 기껏 쿼리 메서드를 호출할 필요 없이 관계를 속성처럼 접근할 수 있습니다. 예를 들어 `User`와 `Post` 예시에서, 사용자 모든 포스트를 아래와 같이 간단하게 조회할 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

foreach ($user->posts as $post) {
    // ...
}
```

<!-- Dynamic relationship properties perform "lazy loading", meaning they will only load their relationship data when you actually access them. Because of this, developers often use [eager loading](#eager-loading) to pre-load relationships they know will be accessed after loading the model. Eager loading provides a significant reduction in SQL queries that must be executed to load a model's relations. -->
동적 관계 속성은 "지연 로딩(lazy loading)" 방식으로 동작합니다. 즉, 실제로 속성에 접근할 때에만 관련 데이터가 쿼리되어 가져옵니다. 이런 이유로, 모델을 미리 로딩한 뒤 곧바로 관계 데이터를 사용할 경우 [eager loading](#eager-loading)을 자주 활용합니다. eager loading은 쿼리 수를 크게 줄여 주므로 성능에 많은 도움이 됩니다.

<a name="querying-relationship-existence"></a>
<!-- ### Querying Relationship Existence -->
### Querying Relationship Existence

<!-- When retrieving model records, you may wish to limit your results based on the existence of a relationship. For example, imagine you want to retrieve all blog posts that have at least one comment. To do so, you may pass the name of the relationship to the `has` and `orHas` methods: -->
모델 레코드를 조회할 때, 특정 관계가 존재하는 경우에만 결과를 제한하고 싶을 수 있습니다. 예를 들어, 최소한 하나 이상의 댓글이 달린 모든 블로그 포스트를 조회하려면, `has` 또는 `orHas` 메서드에 관계명을 인수로 전달하면 됩니다.

```
use App\Models\Post;

// Retrieve all posts that have at least one comment...
$posts = Post::has('comments')->get();
```

<!-- You may also specify an operator and count value to further customize the query: -->
연산자와 수치를 추가로 지정해 조건을 더욱 세밀하게 커스터마이징할 수도 있습니다.

```
// Retrieve all posts that have three or more comments...
$posts = Post::has('comments', '>=', 3)->get();
```

<!-- Nested `has` statements may be constructed using "dot" notation. For example, you may retrieve all posts that have at least one comment that has at least one image: -->
중첩된 `has` 조건은 "닷(dot) 표기법"을 이용해 만들 수 있습니다. 예를 들어, 최소한 하나의 댓글이 있으면서 그 댓글에 최소 하나의 이미지가 있는 포스트를 조회하려면:

```
// Retrieve posts that have at least one comment with images...
$posts = Post::has('comments.images')->get();
```

<!-- If you need even more power, you may use the `whereHas` and `orWhereHas` methods to define additional query constraints on your `has` queries, such as inspecting the content of a comment: -->
더 강력한 쿼리가 필요하다면, `has` 쿼리 안에서 관계의 내용을 검사할 수 있도록 `whereHas` 또는 `orWhereHas` 메서드를 사용할 수 있습니다. 예를 들면:

```
use Illuminate\Database\Eloquent\Builder;

// Retrieve posts with at least one comment containing words like code%...
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();

// Retrieve posts with at least ten comments containing words like code%...
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
}, '>=', 10)->get();
```

> [!WARNING]
> Eloquent에서는 현재 다른 데이터베이스 간 관계 존재 쿼리를 지원하지 않습니다. 관계 모델은 반드시 동일한 데이터베이스 내에 존재해야 합니다.

<a name="inline-relationship-existence-queries"></a>
<!-- #### Inline Relationship Existence Queries -->
#### Inline Relationship Existence Queries

<!-- If you would like to query for a relationship's existence with a single, simple where condition attached to the relationship query, you may find it more convenient to use the `whereRelation`, `orWhereRelation`, `whereMorphRelation`, and `orWhereMorphRelation` methods. For example, we may query for all posts that have unapproved comments: -->
관계의 존재를 간단한 단일 where 조건과 함께 쿼리하고 싶을 때는 `whereRelation`, `orWhereRelation`, `whereMorphRelation`, `orWhereMorphRelation` 메서드가 더욱 편리할 수 있습니다. 예를 들어, 승인되지 않은(unapproved) 댓글이 달린 모든 포스트를 조회하는 예시는 아래와 같습니다.

```
use App\Models\Post;

$posts = Post::whereRelation('comments', 'is_approved', false)->get();
```

<!-- Of course, like calls to the query builder's `where` method, you may also specify an operator: -->
물론, `where` 메서드와 마찬가지로 연산자도 지정할 수 있습니다.

```
$posts = Post::whereRelation(
    'comments', 'created_at', '>=', now()->subHour()
)->get();
```

<a name="querying-relationship-absence"></a>
<!-- ### Querying Relationship Absence -->
### Querying Relationship Absence

<!-- When retrieving model records, you may wish to limit your results based on the absence of a relationship. For example, imagine you want to retrieve all blog posts that **don't** have any comments. To do so, you may pass the name of the relationship to the `doesntHave` and `orDoesntHave` methods: -->
반대로, 특정 관계가 "존재하지 않는" 결과만 조회하고 싶은 경우도 있습니다. 예를 들어, **댓글이 하나도 없는** 모든 블로그 포스트를 조회하려면 `doesntHave`나 `orDoesntHave` 메서드에 관계명을 전달하면 됩니다.

```
use App\Models\Post;

$posts = Post::doesntHave('comments')->get();
```

<!-- If you need even more power, you may use the `whereDoesntHave` and `orWhereDoesntHave` methods to add additional query constraints to your `doesntHave` queries, such as inspecting the content of a comment: -->
더 고급 쿼리가 필요하다면, `doesntHave` 쿼리 내에서 관계 내용을 검사할 수 있도록 `whereDoesntHave` 또는 `orWhereDoesntHave` 메서드를 사용할 수 있습니다.

```
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();
```

<!-- You may use "dot" notation to execute a query against a nested relationship. For example, the following query will retrieve all posts that do not have comments; however, posts that have comments from authors that are not banned will be included in the results: -->
"닷(dot) 표기법"을 사용하면 중첩 관계에도 쿼리를 실행할 수 있습니다. 아래 쿼리는 댓글이 전혀 없는 포스트를 조회하는데, "댓글 작성자가 밴(banned)되지 않은" 경우에는 해당 포스트도 결과에 포함된다는 점에 유의해야 합니다.

```
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments.author', function (Builder $query) {
    $query->where('banned', 0);
})->get();
```

<a name="querying-morph-to-relationships"></a>
<!-- ### Querying Morph To Relationships -->
### Querying Morph To Relationships

<!-- To query the existence of "morph to" relationships, you may use the `whereHasMorph` and `whereDoesntHaveMorph` methods. These methods accept the name of the relationship as their first argument. Next, the methods accept the names of the related models that you wish to include in the query. Finally, you may provide a closure which customizes the relationship query: -->
"Morph To" 관계의 존재 여부를 쿼리할 때는 `whereHasMorph`와 `whereDoesntHaveMorph` 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인수로 관계명을, 그 다음 인수로 쿼리에 포함시킬 관련 모델명을, 그리고 마지막으로 관계 쿼리를 커스터마이징하기 위한 클로저를 받습니다.

```
use App\Models\Comment;
use App\Models\Post;
use App\Models\Video;
use Illuminate\Database\Eloquent\Builder;

// Retrieve comments associated to posts or videos with a title like code%...
$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();

// Retrieve comments associated to posts with a title not like code%...
$comments = Comment::whereDoesntHaveMorph(
    'commentable',
    Post::class,
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();
```

<!-- You may occasionally need to add query constraints based on the "type" of the related polymorphic model. The closure passed to the `whereHasMorph` method may receive a `$type` value as its second argument. This argument allows you to inspect the "type" of the query that is being built: -->
경우에 따라 다형적(parent) 모델의 "타입"에 따라 추가 쿼리 조건을 지정하고 싶을 수도 있습니다. 이럴 때는 `whereHasMorph`에 넘기는 클로저의 두 번째 인수로 `$type` 값을 받을 수 있습니다. 이 값을 이용해 해당 쿼리 대상의 타입에 따라 컬럼이나 조건을 다르게 지정할 수 있습니다.

```
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query, string $type) {
        $column = $type === Post::class ? 'content' : 'title';

        $query->where($column, 'like', 'code%');
    }
)->get();
```

<!-- Sometimes you may want to query for the children of a "morph to" relationship's parent. You may accomplish this using the `whereMorphedTo` and `whereNotMorphedTo` methods, which will automatically determine the proper morph type mapping for the given model. These methods accept the name of the `morphTo` relationship as their first argument and the related parent model as their second argument: -->
경우에 따라 "morph to" 관계의 부모로부터 자식들을 조회하고 싶을 때가 있습니다. 이런 경우에는 `whereMorphedTo`와 `whereNotMorphedTo` 메서드를 활용하면, 해당 모델에 맞는 morph 타입을 자동으로 매핑하여 쿼리를 실행합니다. 이 메서드는 첫 번째 인수로 `morphTo` 관계명, 두 번째 인수로 부모 모델을 받습니다.

```
$comments = Comment::whereMorphedTo('commentable', $post)
    ->orWhereMorphedTo('commentable', $video)
    ->get();
```

<a name="querying-all-morph-to-related-models"></a>

<!-- #### Querying All Related Models -->
#### Querying All Related Models

<!-- Instead of passing an array of possible polymorphic models, you may provide `*` as a wildcard value. This will instruct Laravel to retrieve all of the possible polymorphic types from the database. Laravel will execute an additional query in order to perform this operation: -->
복수의 다형적(polymorphic) 모델 배열 대신, `*`를 와일드카드(wildcard) 값으로 전달할 수 있습니다. 이렇게 하면 Laravel이 데이터베이스에서 가능한 모든 다형적 타입을 조회하도록 지시합니다. 이 작업을 위해 Laravel은 추가 쿼리를 실행하게 됩니다.

```
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph('commentable', '*', function (Builder $query) {
    $query->where('title', 'like', 'foo%');
})->get();
```

<a name="aggregating-related-models"></a>
<!-- ## Aggregating Related Models -->
## Aggregating Related Models

<a name="counting-related-models"></a>
<!-- ### Counting Related Models -->
### Counting Related Models

<!-- Sometimes you may want to count the number of related models for a given relationship without actually loading the models. To accomplish this, you may use the `withCount` method. The `withCount` method will place a `{relation}_count` attribute on the resulting models: -->
특정 관계에 대해 실제로 모델을 로드하지 않고도 관련 모델의 개수를 세고 싶을 때가 있습니다. 이럴 때는 `withCount` 메서드를 사용할 수 있습니다. `withCount` 메서드는 결과 모델에 `{relation}_count` 속성을 추가합니다.

```
use App\Models\Post;

$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->comments_count;
}
```

<!-- By passing an array to the `withCount` method, you may add the "counts" for multiple relations as well as add additional constraints to the queries: -->
`withCount` 메서드에 배열을 전달하면 여러 관계의 "개수"를 추가할 수 있으며, 쿼리에 추가 제약도 걸 수 있습니다.

```
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount(['votes', 'comments' => function (Builder $query) {
    $query->where('content', 'like', 'code%');
}])->get();

echo $posts[0]->votes_count;
echo $posts[0]->comments_count;
```

<!-- You may also alias the relationship count result, allowing multiple counts on the same relationship: -->
또한 관계의 개수 결과에 별칭(alias)을 지정할 수 있어, 같은 관계에 여러 개수를 집계할 수도 있습니다.

```
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount([
    'comments',
    'comments as pending_comments_count' => function (Builder $query) {
        $query->where('approved', false);
    },
])->get();

echo $posts[0]->comments_count;
echo $posts[0]->pending_comments_count;
```

<a name="deferred-count-loading"></a>
<!-- #### Deferred Count Loading -->
#### Deferred Count Loading

<!-- Using the `loadCount` method, you may load a relationship count after the parent model has already been retrieved: -->
`loadCount` 메서드를 사용하면 상위(parent) 모델을 이미 조회한 이후에도 관계의 개수를 로드할 수 있습니다.

```
$book = Book::first();

$book->loadCount('genres');
```

<!-- If you need to set additional query constraints on the count query, you may pass an array keyed by the relationships you wish to count. The array values should be closures which receive the query builder instance: -->
카운트 쿼리에 추가 조건을 걸어야 할 때는, 카운트하고 싶은 관계명을 키로 지정한 배열을 전달합니다. 배열의 값은 쿼리 빌더 인스턴스를 받는 클로저여야 합니다.

```
$book->loadCount(['reviews' => function (Builder $query) {
    $query->where('rating', 5);
}])
```

<a name="relationship-counting-and-custom-select-statements"></a>
<!-- #### Relationship Counting and Custom Select Statements -->
#### Relationship Counting and Custom Select Statements

<!-- If you're combining `withCount` with a `select` statement, ensure that you call `withCount` after the `select` method: -->
`withCount`를 `select` 문과 함께 사용할 경우, 반드시 `select` 메서드 호출 이후에 `withCount`를 호출해야 합니다.

```
$posts = Post::select(['title', 'body'])
    ->withCount('comments')
    ->get();
```

<a name="other-aggregate-functions"></a>
<!-- ### Other Aggregate Functions -->
### Other Aggregate Functions

<!-- In addition to the `withCount` method, Eloquent provides `withMin`, `withMax`, `withAvg`, `withSum`, and `withExists` methods. These methods will place a `{relation}_{function}_{column}` attribute on your resulting models: -->
`withCount` 메서드 외에도, Eloquent는 `withMin`, `withMax`, `withAvg`, `withSum`, `withExists` 등의 메서드를 제공합니다. 이 메서드들은 결과 모델 객체에 `{relation}_{function}_{column}` 형식의 속성을 추가합니다.

```
use App\Models\Post;

$posts = Post::withSum('comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->comments_sum_votes;
}
```

<!-- If you wish to access the result of the aggregate function using another name, you may specify your own alias: -->
집계 함수의 결과를 다른 이름으로 사용하고 싶을 경우, 별칭을 지정할 수 있습니다.

```
$posts = Post::withSum('comments as total_comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->total_comments;
}
```

<!-- Like the `loadCount` method, deferred versions of these methods are also available. These additional aggregate operations may be performed on Eloquent models that have already been retrieved: -->
`loadCount` 메서드처럼, 이미 조회한 Eloquent 모델에서 지연 집계 작업을 할 수도 있습니다.

```
$post = Post::first();

$post->loadSum('comments', 'votes');
```

<!-- If you're combining these aggregate methods with a `select` statement, ensure that you call the aggregate methods after the `select` method: -->
이러한 집계 메서드를 `select` 문과 함께 사용할 때는, 반드시 `select` 후에 집계 메서드를 호출해야 합니다.

```
$posts = Post::select(['title', 'body'])
    ->withExists('comments')
    ->get();
```

<a name="counting-related-models-on-morph-to-relationships"></a>
<!-- ### Counting Related Models on Morph To Relationships -->
### Counting Related Models on Morph To Relationships

<!-- If you would like to eager load a "morph to" relationship, as well as related model counts for the various entities that may be returned by that relationship, you may utilize the `with` method in combination with the `morphTo` relationship's `morphWithCount` method. -->
"morph to" 관계와, 해당 관계로 반환될 수 있는 여러 엔티티의 관련 모델 개수도 사전 로딩(eager load)하고 싶을 때가 있습니다. 이 경우, `with` 메서드와 `morphTo` 관계의 `morphWithCount` 메서드를 조합해 사용할 수 있습니다.

<!-- In this example, let's assume that `Photo` and `Post` models may create `ActivityFeed` models. We will assume the `ActivityFeed` model defines a "morph to" relationship named `parentable` that allows us to retrieve the parent `Photo` or `Post` model for a given `ActivityFeed` instance. Additionally, let's assume that `Photo` models "have many" `Tag` models and `Post` models "have many" `Comment` models. -->
이 예제에서는 `Photo` 모델과 `Post` 모델이 `ActivityFeed` 모델을 생성한다고 가정합니다. 그리고 `ActivityFeed` 모델에 `parentable`이라는 "morph to" 관계가 정의되어 있다고 가정하면, 이는 특정 `ActivityFeed` 인스턴스에 대해 부모 `Photo` 또는 `Post` 모델을 가져올 수 있게 해줍니다. 또한, `Photo` 모델은 다수의 `Tag` 모델과, `Post` 모델은 다수의 `Comment` 모델과 연관되어 있다고 가정합니다.

<!-- Now, let's imagine we want to retrieve `ActivityFeed` instances and eager load the `parentable` parent models for each `ActivityFeed` instance. In addition, we want to retrieve the number of tags that are associated with each parent photo and the number of comments that are associated with each parent post: -->
이제 `ActivityFeed` 인스턴스들을 조회하면서 각 `ActivityFeed` 인스턴스의 부모 모델(`parentable`)을 eager load하고, 해당 부모 포토의 태그 개수와, 부모 포스트의 코멘트 개수도 함께 가져오고자 한다면 아래와 같이 할 수 있습니다.

```
use Illuminate\Database\Eloquent\Relations\MorphTo;

$activities = ActivityFeed::with([
    'parentable' => function (MorphTo $morphTo) {
        $morphTo->morphWithCount([
            Photo::class => ['tags'],
            Post::class => ['comments'],
        ]);
    }])->get();
```

<a name="morph-to-deferred-count-loading"></a>
<!-- #### Deferred Count Loading -->
#### Deferred Count Loading

<!-- Let's assume we have already retrieved a set of `ActivityFeed` models and now we would like to load the nested relationship counts for the various `parentable` models associated with the activity feeds. You may use the `loadMorphCount` method to accomplish this: -->
이미 여러 `ActivityFeed` 모델을 조회했다면, 이후에 이들에 연결된 각기 다른 `parentable` 모델의 내부 관계(태그/댓글 등) 개수도 로드하고 싶을 수 있습니다. 이를 위해 `loadMorphCount` 메서드를 사용할 수 있습니다.

```
$activities = ActivityFeed::with('parentable')->get();

$activities->loadMorphCount('parentable', [
    Photo::class => ['tags'],
    Post::class => ['comments'],
]);
```

<a name="eager-loading"></a>
<!-- ## Eager Loading -->
## Eager Loading

<!-- When accessing Eloquent relationships as properties, the related models are "lazy loaded". This means the relationship data is not actually loaded until you first access the property. However, Eloquent can "eager load" relationships at the time you query the parent model. Eager loading alleviates the "N + 1" query problem. To illustrate the N + 1 query problem, consider a `Book` model that "belongs to" to an `Author` model: -->
Eloquent 관계를 프로퍼티처럼 접근하면, 관련 모델은 "지연 로드(lazy loaded)"됩니다. 즉, 관계 데이터를 처음 접근하기 전까지는 실제로 로드되지 않습니다. 하지만, 부모 모델을 쿼리할 때 "사전 로딩(eager loading)"을 할 수도 있습니다. 사전 로딩은 이른바 "N + 1" 쿼리 문제를 해결합니다. N + 1 쿼리 문제를 보여주는 예로, `Book` 모델이 `Author` 모델에 "belongs to" 관계를 맺고 있다고 가정해봅니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * Get the author that wrote the book.
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }
}
```

<!-- Now, let's retrieve all books and their authors: -->
이제 모든 책과 저자의 정보를 조회한다고 해봅니다.

```
use App\Models\Book;

$books = Book::all();

foreach ($books as $book) {
    echo $book->author->name;
}
```

<!-- This loop will execute one query to retrieve all of the books within the database table, then another query for each book in order to retrieve the book's author. So, if we have 25 books, the code above would run 26 queries: one for the original book, and 25 additional queries to retrieve the author of each book. -->
이 루프는 우선 전체 책 목록을 한 번 쿼리하고, 각 책의 저자를 각각 개별 쿼리로 가져옵니다. 만약 25권의 책이 있다면, 위 코드는 총 26번의 쿼리(책 1번 + 책마다 저자 25번)를 실행합니다.

<!-- Thankfully, we can use eager loading to reduce this operation to just two queries. When building a query, you may specify which relationships should be eager loaded using the `with` method: -->
다행히도, 사전 로딩을 사용하면 쿼리를 단 2번으로 줄일 수 있습니다. 쿼리를 작성할 때 사전에 로딩하고 싶은 관계를 `with` 메서드로 지정하면 됩니다.

```
$books = Book::with('author')->get();

foreach ($books as $book) {
    echo $book->author->name;
}
```

<!-- For this operation, only two queries will be executed - one query to retrieve all of the books and one query to retrieve all of the authors for all of the books: -->
이 과정에서는 단 2번의 쿼리만 실행됩니다. 첫 번째는 모든 책을, 두 번째는 모든 책에 해당하는 저자들을 한 번에 가져오는 쿼리입니다.

```sql
select * from books

select * from authors where id in (1, 2, 3, 4, 5, ...)
```

<a name="eager-loading-multiple-relationships"></a>
<!-- #### Eager Loading Multiple Relationships -->
#### Eager Loading Multiple Relationships

<!-- Sometimes you may need to eager load several different relationships. To do so, just pass an array of relationships to the `with` method: -->
한 번에 여러 관계를 사전 로딩하고 싶다면, `with` 메서드에 관계명을 배열로 전달하면 됩니다.

```
$books = Book::with(['author', 'publisher'])->get();
```

<a name="nested-eager-loading"></a>
<!-- #### Nested Eager Loading -->
#### Nested Eager Loading

<!-- To eager load a relationship's relationships, you may use "dot" syntax. For example, let's eager load all of the book's authors and all of the author's personal contacts: -->
관계의 관계, 즉 중첩 관계까지 사전 로딩하고 싶을 경우 "dot" 문법을 사용할 수 있습니다. 예를 들어, 모든 책의 저자와, 또 저자의 연락처(personal contacts)까지 한 번에 가져오려면 아래와 같이 작성합니다.

```
$books = Book::with('author.contacts')->get();
```

<!-- Alternatively, you may specify nested eager loaded relationships by providing a nested array to the `with` method, which can be convenient when eager loading multiple nested relationships: -->
또는 사전 로딩할 중첩 관계가 많다면, `with` 메서드에 중첩 배열을 사용할 수도 있습니다. 이 방법은 여러 단계의 관계를 더욱 명확하게 작성할 때 유용합니다.

```
$books = Book::with([
    'author' => [
        'contacts',
        'publisher',
    ],
])->get();
```

<a name="nested-eager-loading-morphto-relationships"></a>
<!-- #### Nested Eager Loading `morphTo` Relationships -->
#### Nested Eager Loading `morphTo` Relationships

<!-- If you would like to eager load a `morphTo` relationship, as well as nested relationships on the various entities that may be returned by that relationship, you may use the `with` method in combination with the `morphTo` relationship's `morphWith` method. To help illustrate this method, let's consider the following model: -->
`morphTo` 관계와, 해당 관계로 반환될 수 있는 다양한 엔티티의 중첩 관계 역시 사전 로딩하고 싶을 수 있습니다. 이럴 땐 `with` 메서드를 `morphTo` 관계의 `morphWith` 메서드와 조합해 사용합니다. 이해를 돕기 위해 아래와 같은 모델 구조를 생각해봅니다.

```
<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class ActivityFeed extends Model
{
    /**
     * Get the parent of the activity feed record.
     */
    public function parentable(): MorphTo
    {
        return $this->morphTo();
    }
}
```

<!-- In this example, let's assume `Event`, `Photo`, and `Post` models may create `ActivityFeed` models. Additionally, let's assume that `Event` models belong to a `Calendar` model, `Photo` models are associated with `Tag` models, and `Post` models belong to an `Author` model. -->
이 예시에서는 `Event`, `Photo`, `Post` 모델이 모두 `ActivityFeed` 모델을 생성할 수 있다고 가정합니다. 또한, `Event` 모델은 `Calendar` 모델과, `Photo`는 `Tag` 모델과, `Post`는 `Author` 모델과 각각 관계가 있다고 가정합니다.

<!-- Using these model definitions and relationships, we may retrieve `ActivityFeed` model instances and eager load all `parentable` models and their respective nested relationships: -->
이런 모델 구조를 바탕으로, `ActivityFeed` 모델 인스턴스를 가져오면서 각 `parentable` 모델과, 그에 대한 중첩 관계까지 모두 사전 로딩하고 싶다면 아래와 같이 하면 됩니다.

```
use Illuminate\Database\Eloquent\Relations\MorphTo;

$activities = ActivityFeed::query()
    ->with(['parentable' => function (MorphTo $morphTo) {
        $morphTo->morphWith([
            Event::class => ['calendar'],
            Photo::class => ['tags'],
            Post::class => ['author'],
        ]);
    }])->get();
```

<a name="eager-loading-specific-columns"></a>
<!-- #### Eager Loading Specific Columns -->
#### Eager Loading Specific Columns

<!-- You may not always need every column from the relationships you are retrieving. For this reason, Eloquent allows you to specify which columns of the relationship you would like to retrieve: -->
관계에서 모든 컬럼이 필요하지 않을 수도 있습니다. 이런 경우, Eloquent의 기능을 사용해 원하는 컬럼만 선택적으로 가져올 수 있습니다.

```
$books = Book::with('author:id,name,book_id')->get();
```

> [!WARNING]
> 이 기능을 사용할 때는 반드시 `id` 컬럼과, 필요한 경우 외래 키(foreign key) 컬럼도 목록에 포함해야 합니다.

<a name="eager-loading-by-default"></a>
<!-- #### Eager Loading by Default -->
#### Eager Loading by Default

<!-- Sometimes you might want to always load some relationships when retrieving a model. To accomplish this, you may define a `$with` property on the model: -->
특정 모델을 조회할 때 항상 일부 관계도 함께 로드하고 싶다면, 모델에 `$with` 프로퍼티를 정의하면 됩니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * The relationships that should always be loaded.
     *
     * @var array
     */
    protected $with = ['author'];

    /**
     * Get the author that wrote the book.
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }

    /**
     * Get the genre of the book.
     */
    public function genre(): BelongsTo
    {
        return $this->belongsTo(Genre::class);
    }
}
```

<!-- If you would like to remove an item from the `$with` property for a single query, you may use the `without` method: -->
단일 쿼리에서 `$with` 프로퍼티에 등록된 관계 중 일부만 제거하고 싶을 때는 `without` 메서드를 사용할 수 있습니다.

```
$books = Book::without('author')->get();
```

<!-- If you would like to override all items within the `$with` property for a single query, you may use the `withOnly` method: -->
특정 쿼리에서 `$with`에 포함된 모든 관계를 대체하고 싶으면, `withOnly` 메서드를 사용합니다.

```
$books = Book::withOnly('genre')->get();
```

<a name="constraining-eager-loads"></a>
<!-- ### Constraining Eager Loads -->
### Constraining Eager Loads

<!-- Sometimes you may wish to eager load a relationship but also specify additional query conditions for the eager loading query. You can accomplish this by passing an array of relationships to the `with` method where the array key is a relationship name and the array value is a closure that adds additional constraints to the eager loading query: -->
관계를 eager load 하면서 쿼리에 추가 제약조건도 걸고 싶을 때가 있습니다. 이럴 때는 `with` 메서드에 관계명과 함께, 추가 제약조건을 정의한 클로저를 값으로 가지는 배열을 전달하면 됩니다.

```
use App\Models\User;
use Illuminate\Contracts\Database\Eloquent\Builder;

$users = User::with(['posts' => function (Builder $query) {
    $query->where('title', 'like', '%code%');
}])->get();
```

<!-- In this example, Eloquent will only eager load posts where the post's `title` column contains the word `code`. You may call other [query builder](/docs/11.x/queries) methods to further customize the eager loading operation: -->
이 예제에서는 게시글의 `title` 컬럼에 `code`라는 단어가 포함된 경우에만 posts 관계가 eager load 됩니다. [query builder](/docs/11.x/queries)에서 제공하는 다른 메서드도 자유롭게 사용할 수 있습니다.

```
$users = User::with(['posts' => function (Builder $query) {
    $query->orderBy('created_at', 'desc');
}])->get();
```

<a name="constraining-eager-loading-of-morph-to-relationships"></a>
<!-- #### Constraining Eager Loading of `morphTo` Relationships -->
#### Constraining Eager Loading of `morphTo` Relationships

<!-- If you are eager loading a `morphTo` relationship, Eloquent will run multiple queries to fetch each type of related model. You may add additional constraints to each of these queries using the `MorphTo` relation's `constrain` method: -->
`morphTo` 관계를 eager load 할 때, Eloquent는 각 관련 모델 타입마다 각각 쿼리를 실행합니다. 각 쿼리에 추가 조건을 걸고 싶다면, `MorphTo` 관계의 `constrain` 메서드를 사용할 수 있습니다.

```
use Illuminate\Database\Eloquent\Relations\MorphTo;

$comments = Comment::with(['commentable' => function (MorphTo $morphTo) {
    $morphTo->constrain([
        Post::class => function ($query) {
            $query->whereNull('hidden_at');
        },
        Video::class => function ($query) {
            $query->where('type', 'educational');
        },
    ]);
}])->get();
```

<!-- In this example, Eloquent will only eager load posts that have not been hidden and videos that have a `type` value of "educational". -->
위 예제의 경우, Eloquent는 숨김 처리되지 않은 포스트와, `type` 값이 "educational"인 비디오만 eager load 합니다.

<a name="constraining-eager-loads-with-relationship-existence"></a>
<!-- #### Constraining Eager Loads With Relationship Existence -->
#### Constraining Eager Loads With Relationship Existence

<!-- You may sometimes find yourself needing to check for the existence of a relationship while simultaneously loading the relationship based on the same conditions. For example, you may wish to only retrieve `User` models that have child `Post` models matching a given query condition while also eager loading the matching posts. You may accomplish this using the `withWhereHas` method: -->
관계의 존재 여부를 체크하면서 동시에 동일 조건으로 관계를 eager load 해야 하는 경우도 있습니다. 예를 들어, 특정 조건을 만족하는 하위 `Post` 모델이 존재하는 `User` 모델만 조회하면서, 조건에 맞는 posts만 함께 eager load하고 싶을 때는 `withWhereHas` 메서드를 활용할 수 있습니다.

```
use App\Models\User;

$users = User::withWhereHas('posts', function ($query) {
    $query->where('featured', true);
})->get();
```

<a name="lazy-eager-loading"></a>
<!-- ### Lazy Eager Loading -->
### Lazy Eager Loading

<!-- Sometimes you may need to eager load a relationship after the parent model has already been retrieved. For example, this may be useful if you need to dynamically decide whether to load related models: -->
이미 상위(parent) 모델을 조회한 후에 관계를 사전 로딩해야 할 때도 있습니다. 예를 들어, 관계 데이터를 로드할 필요가 있는지 동적으로 결정해야 할 경우에 유용합니다.

```
use App\Models\Book;

$books = Book::all();

if ($someCondition) {
    $books->load('author', 'publisher');
}
```

<!-- If you need to set additional query constraints on the eager loading query, you may pass an array keyed by the relationships you wish to load. The array values should be closure instances which receive the query instance: -->
eager loading 쿼리에 추가 제약을 걸고 싶다면, 로드하고 싶은 관계명을 키로 한 배열을 전달하면 됩니다. 배열의 값은 쿼리 인스턴스를 받는 클로저여야 합니다.

```
$author->load(['books' => function (Builder $query) {
    $query->orderBy('published_date', 'asc');
}]);
```

<!-- To load a relationship only when it has not already been loaded, use the `loadMissing` method: -->
관계가 아직 로드되지 않은 경우에만 로드하려면, `loadMissing` 메서드를 사용하세요.

```
$book->loadMissing('author');
```

<a name="nested-lazy-eager-loading-morphto"></a>
<!-- #### Nested Lazy Eager Loading and `morphTo` -->
#### Nested Lazy Eager Loading and `morphTo`

<!-- If you would like to eager load a `morphTo` relationship, as well as nested relationships on the various entities that may be returned by that relationship, you may use the `loadMorph` method. -->
`morphTo` 관계와, 해당 관계로 반환될 수 있는 여러 엔티티의 중첩 관계까지 지연 로딩하고 싶을 경우 `loadMorph` 메서드를 사용할 수 있습니다.

<!-- This method accepts the name of the `morphTo` relationship as its first argument, and an array of model / relationship pairs as its second argument. To help illustrate this method, let's consider the following model: -->
이 메서드는 첫 번째 인자로 `morphTo` 관계명을, 두 번째 인자로 모델/관계 쌍의 배열을 받습니다. 이해를 돕기 위해 아래와 같은 모델 구조를 참고하세요.

```
<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class ActivityFeed extends Model
{
    /**
     * Get the parent of the activity feed record.
     */
    public function parentable(): MorphTo
    {
        return $this->morphTo();
    }
}
```

<!-- In this example, let's assume `Event`, `Photo`, and `Post` models may create `ActivityFeed` models. Additionally, let's assume that `Event` models belong to a `Calendar` model, `Photo` models are associated with `Tag` models, and `Post` models belong to an `Author` model. -->
예를 들어, `Event`, `Photo`, `Post` 모델이 모두 `ActivityFeed` 모델을 만들 수 있다고 가정합니다. 또한 `Event` 모델은 `Calendar` 모델에 속하고, `Photo` 모델은 `Tag` 모델과 연관되며, `Post` 모델은 `Author` 모델에 속한다고 가정합니다.

<!-- Using these model definitions and relationships, we may retrieve `ActivityFeed` model instances and eager load all `parentable` models and their respective nested relationships: -->
이 경우, 다음과 같이 `ActivityFeed` 모델 인스턴스를 조회한 후 모든 `parentable` 모델과 각 모델의 중첩 관계도 즉시 로딩할 수 있습니다.

```
$activities = ActivityFeed::with('parentable')
    ->get()
    ->loadMorph('parentable', [
        Event::class => ['calendar'],
        Photo::class => ['tags'],
        Post::class => ['author'],
    ]);
```

<a name="preventing-lazy-loading"></a>
<!-- ### Preventing Lazy Loading -->
### Preventing Lazy Loading

<!-- As previously discussed, eager loading relationships can often provide significant performance benefits to your application. Therefore, if you would like, you may instruct Laravel to always prevent the lazy loading of relationships. To accomplish this, you may invoke the `preventLazyLoading` method offered by the base Eloquent model class. Typically, you should call this method within the `boot` method of your application's `AppServiceProvider` class. -->
앞서 언급했듯, 관계의 사전 로딩은 애플리케이션 성능에 큰 도움이 됩니다. 따라서, 원한다면 Laravel이 관계의 지연 로딩을 아예 차단하도록 만들 수도 있습니다. 이를 위해서는 기본 Eloquent 모델 클래스가 제공하는 `preventLazyLoading` 메서드를 사용하세요. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출하게 됩니다.

<!-- The `preventLazyLoading` method accepts an optional boolean argument that indicates if lazy loading should be prevented. For example, you may wish to only disable lazy loading in non-production environments so that your production environment will continue to function normally even if a lazy loaded relationship is accidentally present in production code: -->
`preventLazyLoading` 메서드는 옵션으로 불리언 값을 받을 수 있으며, 이 값에 따라 지연 로딩 금지 여부를 제어합니다. 예를 들어, 운영 환경(production) 이외에서만 지연 로딩을 차단하고 싶다면 아래처럼 작성할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

<!-- After preventing lazy loading, Eloquent will throw a `Illuminate\Database\LazyLoadingViolationException` exception when your application attempts to lazy load any Eloquent relationship. -->
지연 로딩이 차단된 상태에서 Eloquent 관계를 지연 로딩하려 하면, Laravel은 `Illuminate\Database\LazyLoadingViolationException` 예외를 발생시킵니다.

<!-- You may customize the behavior of lazy loading violations using the `handleLazyLoadingViolationsUsing` method. For example, using this method, you may instruct lazy loading violations to only be logged instead of interrupting the application's execution with exceptions: -->
지연 로딩 위반 시 동작을 커스터마이즈하려면, `handleLazyLoadingViolationsUsing` 메서드를 활용할 수 있습니다. 예를 들어, 예외로 인해 실행이 중단되지 않고 로그만 남도록 설정할 수 있습니다.

```php
Model::handleLazyLoadingViolationUsing(function (Model $model, string $relation) {
    $class = $model::class;

    info("Attempted to lazy load [{$relation}] on model [{$class}].");
});
```

<a name="inserting-and-updating-related-models"></a>
<!-- ## Inserting and Updating Related Models -->
## Inserting and Updating Related Models

<a name="the-save-method"></a>
<!-- ### The `save` Method -->
### The `save` Method

<!-- Eloquent provides convenient methods for adding new models to relationships. For example, perhaps you need to add a new comment to a post. Instead of manually setting the `post_id` attribute on the `Comment` model you may insert the comment using the relationship's `save` method: -->
Eloquent는 관계에 새로운 모델을 추가하는 편리한 메서드들을 제공합니다. 예를 들어, 게시글(Post)에 새로운 코멘트를 추가하고 싶다면, `Comment` 모델에서 직접 `post_id` 속성을 설정하지 않고도, 관계의 `save` 메서드를 이용해 코멘트를 추가할 수 있습니다.

```
use App\Models\Comment;
use App\Models\Post;

$comment = new Comment(['message' => 'A new comment.']);

$post = Post::find(1);

$post->comments()->save($comment);
```

<!-- Note that we did not access the `comments` relationship as a dynamic property. Instead, we called the `comments` method to obtain an instance of the relationship. The `save` method will automatically add the appropriate `post_id` value to the new `Comment` model. -->
여기서 `comments` 관계를 동적 프로퍼티로 접근하지 않고, `comments` 메서드를 호출해 관계 인스턴스를 얻은 점을 확인하세요. `save` 메서드는 새로운 `Comment` 모델에 적절한 `post_id` 값을 자동으로 추가해줍니다.

<!-- If you need to save multiple related models, you may use the `saveMany` method: -->
여러 개의 관련 모델을 저장하려면, `saveMany` 메서드를 사용할 수 있습니다.

```
$post = Post::find(1);

$post->comments()->saveMany([
    new Comment(['message' => 'A new comment.']),
    new Comment(['message' => 'Another new comment.']),
]);
```

<!-- The `save` and `saveMany` methods will persist the given model instances, but will not add the newly persisted models to any in-memory relationships that are already loaded onto the parent model. If you plan on accessing the relationship after using the `save` or `saveMany` methods, you may wish to use the `refresh` method to reload the model and its relationships: -->
`save`와 `saveMany` 메서드는 해당 모델 인스턴스는 저장하지만, 상위 모델에 이미 로드된 관계(메모리 내)의 데이터에는 새로 추가된 모델을 덧붙이지 않습니다. `save`나 `saveMany` 메서드를 사용한 뒤에 관계를 다시 접근해야 한다면, `refresh` 메서드를 사용해 상위 모델과 관계를 다시 불러오는 것이 좋습니다.

```
$post->comments()->save($comment);

$post->refresh();

// All comments, including the newly saved comment...
$post->comments;
```

<a name="the-push-method"></a>
<!-- #### Recursively Saving Models and Relationships -->
#### Recursively Saving Models and Relationships

<!-- If you would like to `save` your model and all of its associated relationships, you may use the `push` method. In this example, the `Post` model will be saved as well as its comments and the comment's authors: -->
모델과 그에 연결된 모든 관계까지 한 번에 `save` 하고 싶다면 `push` 메서드를 사용하면 됩니다. 아래 예제에서는 `Post` 모델, 해당 포스트의 코멘트, 코멘트의 저자까지 모두 한 번에 저장됩니다.

```
$post = Post::find(1);

$post->comments[0]->message = 'Message';
$post->comments[0]->author->name = 'Author Name';

$post->push();
```

<!-- The `pushQuietly` method may be used to save a model and its associated relationships without raising any events: -->
이벤트를 발생시키지 않고 모델과 관계를 저장해야 한다면, `pushQuietly` 메서드를 사용할 수 있습니다.

```
$post->pushQuietly();
```

<a name="the-create-method"></a>

<!-- ### The `create` Method -->
### The `create` Method

<!-- In addition to the `save` and `saveMany` methods, you may also use the `create` method, which accepts an array of attributes, creates a model, and inserts it into the database. The difference between `save` and `create` is that `save` accepts a full Eloquent model instance while `create` accepts a plain PHP `array`. The newly created model will be returned by the `create` method: -->
`save`와 `saveMany` 메서드 외에도, `create` 메서드를 사용할 수 있습니다. 이 메서드는 속성(attribute) 배열을 받아 모델을 생성한 뒤 데이터베이스에 저장합니다. `save`와 `create`의 차이점은, `save`는 전체 Eloquent 모델 인스턴스를 받지만, `create`는 일반 PHP `array`를 받는다는 점입니다. `create` 메서드는 새로 생성된 모델을 반환합니다.

```
use App\Models\Post;

$post = Post::find(1);

$comment = $post->comments()->create([
    'message' => 'A new comment.',
]);
```

<!-- You may use the `createMany` method to create multiple related models: -->
여러 관련 모델을 한 번에 생성하고 싶다면 `createMany` 메서드를 사용할 수 있습니다.

```
$post = Post::find(1);

$post->comments()->createMany([
    ['message' => 'A new comment.'],
    ['message' => 'Another new comment.'],
]);
```

<!-- The `createQuietly` and `createManyQuietly` methods may be used to create a model(s) without dispatching any events: -->
이벤트를 발생시키지 않고 모델을 생성하려면 `createQuietly`와 `createManyQuietly` 메서드를 사용할 수 있습니다.

```
$user = User::find(1);

$user->posts()->createQuietly([
    'title' => 'Post title.',
]);

$user->posts()->createManyQuietly([
    ['title' => 'First post.'],
    ['title' => 'Second post.'],
]);
```

<!-- You may also use the `findOrNew`, `firstOrNew`, `firstOrCreate`, and `updateOrCreate` methods to [create and update models on relationships](/docs/11.x/eloquent#upserts). -->
또한 관계에서 [create and update models on relationships](/docs/11.x/eloquent#upserts)할 때 `findOrNew`, `firstOrNew`, `firstOrCreate`, `updateOrCreate` 메서드를 사용할 수도 있습니다.

> [!NOTE]
> `create` 메서드를 사용하기 전에 [mass assignment](/docs/11.x/eloquent#mass-assignment) 관련 문서를 반드시 참고하시기 바랍니다.

<a name="updating-belongs-to-relationships"></a>
<!-- ### Belongs To Relationships -->
### Belongs To Relationships

<!-- If you would like to assign a child model to a new parent model, you may use the `associate` method. In this example, the `User` model defines a `belongsTo` relationship to the `Account` model. This `associate` method will set the foreign key on the child model: -->
자식 모델을 새로운 부모 모델에 할당하려면 `associate` 메서드를 사용할 수 있습니다. 예를 들어 `User` 모델이 `Account` 모델과 `belongsTo` 관계를 가지고 있다면, `associate` 메서드는 자식 모델의 외래 키를 설정해줍니다.

```
use App\Models\Account;

$account = Account::find(10);

$user->account()->associate($account);

$user->save();
```

<!-- To remove a parent model from a child model, you may use the `dissociate` method. This method will set the relationship's foreign key to `null`: -->
자식 모델에서 부모 모델을 해제하려면 `dissociate` 메서드를 사용하면 됩니다. 이 메서드는 관계의 외래 키를 `null`로 설정합니다.

```
$user->account()->dissociate();

$user->save();
```

<a name="updating-many-to-many-relationships"></a>
<!-- ### Many to Many Relationships -->
### Many to Many Relationships

<a name="attaching-detaching"></a>
<!-- #### Attaching / Detaching -->
#### Attaching / Detaching

<!-- Eloquent also provides methods to make working with many-to-many relationships more convenient. For example, let's imagine a user can have many roles and a role can have many users. You may use the `attach` method to attach a role to a user by inserting a record in the relationship's intermediate table: -->
Eloquent는 다대다(many-to-many) 관계를 더욱 편리하게 다룰 수 있도록 여러 메서드를 제공합니다. 예를 들어, 한 사용자가 여러 역할(role)을 가질 수 있고, 한 역할도 여러 사용자를 가질 수 있다고 가정해봅시다. 이때 `attach` 메서드를 사용하면 관계의 중간 테이블에 새로운 레코드를 추가하여 사용자의 역할을 연결할 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

$user->roles()->attach($roleId);
```

<!-- When attaching a relationship to a model, you may also pass an array of additional data to be inserted into the intermediate table: -->
관계를 연결할 때, 추가로 중간 테이블에 저장할 데이터를 배열로 전달할 수도 있습니다.

```
$user->roles()->attach($roleId, ['expires' => $expires]);
```

<!-- Sometimes it may be necessary to remove a role from a user. To remove a many-to-many relationship record, use the `detach` method. The `detach` method will delete the appropriate record out of the intermediate table; however, both models will remain in the database: -->
역할을 사용자로부터 제거해야 할 때도 있습니다. 다대다 관계의 레코드를 제거하려면 `detach` 메서드를 사용하면 됩니다. `detach` 메서드는 중간 테이블에서 해당 레코드를 삭제하며, 두 모델 자체는 데이터베이스에서 삭제되지 않습니다.

```
// Detach a single role from the user...
$user->roles()->detach($roleId);

// Detach all roles from the user...
$user->roles()->detach();
```

<!-- For convenience, `attach` and `detach` also accept arrays of IDs as input: -->
편의를 위해, `attach`와 `detach`는 ID 배열도 입력으로 받을 수 있습니다.

```
$user = User::find(1);

$user->roles()->detach([1, 2, 3]);

$user->roles()->attach([
    1 => ['expires' => $expires],
    2 => ['expires' => $expires],
]);
```

<a name="syncing-associations"></a>
<!-- #### Syncing Associations -->
#### Syncing Associations

<!-- You may also use the `sync` method to construct many-to-many associations. The `sync` method accepts an array of IDs to place on the intermediate table. Any IDs that are not in the given array will be removed from the intermediate table. So, after this operation is complete, only the IDs in the given array will exist in the intermediate table: -->
다대다 관계를 관리할 때 `sync` 메서드를 사용할 수도 있습니다. `sync`는 관계의 중간 테이블에 남길 ID들의 배열을 받아, 해당 배열에 없는 ID들은 중간 테이블에서 삭제합니다. 즉, 이 작업이 끝나면 중간 테이블에는 지정한 ID만 남게 됩니다.

```
$user->roles()->sync([1, 2, 3]);
```

<!-- You may also pass additional intermediate table values with the IDs: -->
ID와 함께 중간 테이블에 저장할 추가 데이터도 함께 전달할 수 있습니다.

```
$user->roles()->sync([1 => ['expires' => true], 2, 3]);
```

<!-- If you would like to insert the same intermediate table values with each of the synced model IDs, you may use the `syncWithPivotValues` method: -->
만약 동기화하는 모든 ID에 같은 중간 테이블 값을 추가하고 싶다면 `syncWithPivotValues` 메서드를 사용할 수 있습니다.

```
$user->roles()->syncWithPivotValues([1, 2, 3], ['active' => true]);
```

<!-- If you do not want to detach existing IDs that are missing from the given array, you may use the `syncWithoutDetaching` method: -->
지정한 배열에 존재하지 않는 ID를 중간 테이블에서 삭제하고 싶지 않다면 `syncWithoutDetaching` 메서드를 사용할 수 있습니다.

```
$user->roles()->syncWithoutDetaching([1, 2, 3]);
```

<a name="toggling-associations"></a>
<!-- #### Toggling Associations -->
#### Toggling Associations

<!-- The many-to-many relationship also provides a `toggle` method which "toggles" the attachment status of the given related model IDs. If the given ID is currently attached, it will be detached. Likewise, if it is currently detached, it will be attached: -->
다대다 관계에서는 `toggle` 메서드도 제공되며, 이는 전달한 관련 모델 ID의 연결 상태를 "토글"합니다. 즉, 해당 ID가 이미 연결되어 있으면 연결을 해제하고, 연결되어 있지 않으면 연결합니다.

```
$user->roles()->toggle([1, 2, 3]);
```

<!-- You may also pass additional intermediate table values with the IDs: -->
ID와 함께 중간 테이블에 저장할 추가 데이터도 함께 전달할 수 있습니다.

```
$user->roles()->toggle([
    1 => ['expires' => true],
    2 => ['expires' => true],
]);
```

<a name="updating-a-record-on-the-intermediate-table"></a>
<!-- #### Updating a Record on the Intermediate Table -->
#### Updating a Record on the Intermediate Table

<!-- If you need to update an existing row in your relationship's intermediate table, you may use the `updateExistingPivot` method. This method accepts the intermediate record foreign key and an array of attributes to update: -->
관계의 중간 테이블의 기존 행을 업데이트해야 한다면, `updateExistingPivot` 메서드를 사용할 수 있습니다. 이 메서드는 중간 테이블의 외래 키와 함께 업데이트할 속성 배열을 받습니다.

```
$user = User::find(1);

$user->roles()->updateExistingPivot($roleId, [
    'active' => false,
]);
```

<a name="touching-parent-timestamps"></a>
<!-- ## Touching Parent Timestamps -->
## Touching Parent Timestamps

<!-- When a model defines a `belongsTo` or `belongsToMany` relationship to another model, such as a `Comment` which belongs to a `Post`, it is sometimes helpful to update the parent's timestamp when the child model is updated. -->
모델이 `belongsTo` 또는 `belongsToMany` 관계를 통해 다른 모델과 연결되어 있는 경우(예: `Comment` 모델이 `Post` 모델에 소속된 경우), 자식 모델이 업데이트될 때 부모 모델의 타임스탬프를 함께 갱신하면 유용한 경우가 있습니다.

<!-- For example, when a `Comment` model is updated, you may want to automatically "touch" the `updated_at` timestamp of the owning `Post` so that it is set to the current date and time. To accomplish this, you may add a `touches` property to your child model containing the names of the relationships that should have their `updated_at` timestamps updated when the child model is updated: -->
예를 들어, `Comment` 모델이 업데이트될 때, 그에 소속된 `Post`의 `updated_at` 타임스탬프를 현재 일시로 자동 갱신하고 싶을 수 있습니다. 이를 위해 자식 모델에 `touches` 속성을 추가하고, 자식 모델이 업데이트될 때 `updated_at` 타임스탬프를 함께 갱신할 관계의 이름을 배열로 지정하면 됩니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * All of the relationships to be touched.
     *
     * @var array
     */
    protected $touches = ['post'];

    /**
     * Get the post that the comment belongs to.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

> [!WARNING]
> 부모 모델의 타임스탬프는 자식 모델을 Eloquent의 `save` 메서드로 업데이트할 때에만 갱신됩니다.