<!-- # Eloquent: Relationships -->
# Eloquent: Relationships

- [Introduction](#introduction)
- [Defining Relationships](#defining-relationships)
    - [One To One](#one-to-one)
    - [One To Many](#one-to-many)
    - [One To Many (Inverse) / Belongs To](#one-to-many-inverse)
    - [Has One Of Many](#has-one-of-many)
    - [Has One Through](#has-one-through)
    - [Has Many Through](#has-many-through)
- [Many To Many Relationships](#many-to-many)
    - [Retrieving Intermediate Table Columns](#retrieving-intermediate-table-columns)
    - [Filtering Queries Via Intermediate Table Columns](#filtering-queries-via-intermediate-table-columns)
    - [Ordering Queries Via Intermediate Table Columns](#ordering-queries-via-intermediate-table-columns)
    - [Defining Custom Intermediate Table Models](#defining-custom-intermediate-table-models)
- [Polymorphic Relationships](#polymorphic-relationships)
    - [One To One](#one-to-one-polymorphic-relations)
    - [One To Many](#one-to-many-polymorphic-relations)
    - [One Of Many](#one-of-many-polymorphic-relations)
    - [Many To Many](#many-to-many-polymorphic-relations)
    - [Custom Polymorphic Types](#custom-polymorphic-types)
- [Dynamic Relationships](#dynamic-relationships)
- [Querying Relations](#querying-relations)
    - [Relationship Methods Vs. Dynamic Properties](#relationship-methods-vs-dynamic-properties)
    - [Querying Relationship Existence](#querying-relationship-existence)
    - [Querying Relationship Absence](#querying-relationship-absence)
    - [Querying Morph To Relationships](#querying-morph-to-relationships)
- [Aggregating Related Models](#aggregating-related-models)
    - [Counting Related Models](#counting-related-models)
    - [Other Aggregate Functions](#other-aggregate-functions)
    - [Counting Related Models On Morph To Relationships](#counting-related-models-on-morph-to-relationships)
- [Eager Loading](#eager-loading)
    - [Constraining Eager Loads](#constraining-eager-loads)
    - [Lazy Eager Loading](#lazy-eager-loading)
    - [Preventing Lazy Loading](#preventing-lazy-loading)
- [Inserting & Updating Related Models](#inserting-and-updating-related-models)
    - [The `save` Method](#the-save-method)
    - [The `create` Method](#the-create-method)
    - [Belongs To Relationships](#updating-belongs-to-relationships)
    - [Many To Many Relationships](#updating-many-to-many-relationships)
- [Touching Parent Timestamps](#touching-parent-timestamps)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Database tables are often related to one another. For example, a blog post may have many comments or an order could be related to the user who placed it. Eloquent makes managing and working with these relationships easy, and supports a variety of common relationships: -->
데이터베이스 테이블은 서로 연관되어 있는 경우가 많습니다. 예를 들어, 블로그 게시글은 여러 개의 댓글을 가질 수 있고, 하나의 주문은 그 주문을 생성한 사용자와 연관될 수 있습니다. Eloquent를 사용하면 이러한 관계를 쉽고 효율적으로 관리할 수 있으며, 아래와 같은 다양한 일반적인 관계 유형을 지원합니다.

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

<!-- Eloquent relationships are defined as methods on your Eloquent model classes. Since relationships also serve as powerful [query builders](/docs/9.x/queries), defining relationships as methods provides powerful method chaining and querying capabilities. For example, we may chain additional query constraints on this `posts` relationship: -->
Eloquent의 관계는 여러분의 Eloquent 모델 클래스에서 메서드로 정의합니다. 관계는 동시에 강력한 [query builders](/docs/9.x/queries)이기도 하므로, 메서드 형태로 관계를 정의하면 메서드 체이닝 및 쿼리 조작을 자유롭게 활용할 수 있습니다. 예를 들어, 아래와 같이 `posts` 관계에 추가적인 쿼리 조건을 쉽게 체이닝할 수 있습니다.

```
$user->posts()->where('active', 1)->get();
```

<!-- But, before diving too deep into using relationships, let's learn how to define each type of relationship supported by Eloquent. -->
각 관계별 자세한 사용 방법을 살펴보기 전에, Eloquent에서 지원하는 다양한 관계 타입을 정의하는 방법부터 알아보겠습니다.

<a name="one-to-one"></a>
<!-- ### One To One -->
### One To One

<!-- A one-to-one relationship is a very basic type of database relationship. For example, a `User` model might be associated with one `Phone` model. To define this relationship, we will place a `phone` method on the `User` model. The `phone` method should call the `hasOne` method and return its result. The `hasOne` method is available to your model via the model's `Illuminate\Database\Eloquent\Model` base class: -->
일대일 관계는 가장 기본적인 데이터베이스 관계 중 하나입니다. 예를 들어, `User` 모델이 하나의 `Phone` 모델과 연관될 수 있습니다. 이런 관계를 정의하려면 `User` 모델에 `phone` 메서드를 만들고, 이 `phone` 메서드에서 `hasOne` 메서드를 호출한 결과를 반환하면 됩니다. `hasOne` 메서드는 모델의 `Illuminate\Database\Eloquent\Model` 기본 클래스에서 제공됩니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the phone associated with the user.
     */
    public function phone()
    {
        return $this->hasOne(Phone::class);
    }
}
```

<!-- The first argument passed to the `hasOne` method is the name of the related model class. Once the relationship is defined, we may retrieve the related record using Eloquent's dynamic properties. Dynamic properties allow you to access relationship methods as if they were properties defined on the model: -->
`hasOne` 메서드의 첫 번째 인수는 연관 모델 클래스명을 전달합니다. 이 관계가 정의되고 나면, Eloquent의 동적 프로퍼티 기능을 사용해 관련 레코드를 간편하게 불러올 수 있습니다. 동적 프로퍼티란, 관계 메서드를 마치 모델의 속성처럼 접근하는 기능을 의미합니다.

```
$phone = User::find(1)->phone;
```

<!-- Eloquent determines the foreign key of the relationship based on the parent model name. In this case, the `Phone` model is automatically assumed to have a `user_id` foreign key. If you wish to override this convention, you may pass a second argument to the `hasOne` method: -->
Eloquent는 기본적으로 부모 모델명을 기준으로 관계의 외래 키(foreign key)를 결정합니다. 위 예제에서는 `Phone` 모델에 `user_id` 외래 키가 있다고 자동으로 간주합니다. 만약 이 규칙을 오버라이드하고 싶을 경우, `hasOne`의 두 번째 인수로 원하는 외래 키 컬럼을 지정할 수 있습니다.

```
return $this->hasOne(Phone::class, 'foreign_key');
```

<!-- Additionally, Eloquent assumes that the foreign key should have a value matching the primary key column of the parent. In other words, Eloquent will look for the value of the user's `id` column in the `user_id` column of the `Phone` record. If you would like the relationship to use a primary key value other than `id` or your model's `$primaryKey` property, you may pass a third argument to the `hasOne` method: -->
또한, Eloquent는 기본적으로 부모 모델의 프라이머리 키(primary key) 컬럼 값을 외래 키와 매칭합니다. 즉, 위 예제에서는 사용자의 `id` 컬럼의 값이 `Phone` 모델의 `user_id` 컬럼에 저장되어 있다고 간주합니다. 만약 `id`가 아닌 다른 컬럼을 프라이머리 키로 활용하거나, `$primaryKey` 속성을 별도로 지정하고 싶다면, `hasOne`의 세 번째 인수로 로컬(부모) 키 컬럼명을 넘기면 됩니다.

```
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
<!-- #### Defining The Inverse Of The Relationship -->
#### Defining The Inverse Of The Relationship

<!-- So, we can access the `Phone` model from our `User` model. Next, let's define a relationship on the `Phone` model that will let us access the user that owns the phone. We can define the inverse of a `hasOne` relationship using the `belongsTo` method: -->
이제 `User` 모델에서 `Phone` 모델에 접근하는 방법을 알아보았습니다. 이번에는 반대로, `Phone` 모델에서 자신이 속한 사용자(User)에 접근하는 관계를 정의해보겠습니다. `hasOne` 관계의 역방향(즉, 소유자를 찾는 쪽)은 `belongsTo` 메서드를 이용하여 정의합니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Phone extends Model
{
    /**
     * Get the user that owns the phone.
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
```

<!-- When invoking the `user` method, Eloquent will attempt to find a `User` model that has an `id` which matches the `user_id` column on the `Phone` model. -->
이제 `user` 메서드를 호출하면, Eloquent는 `Phone` 모델의 `user_id` 컬럼 값과 일치하는 `User` 모델의 `id` 값을 가진 레코드를 찾아 반환합니다.

<!-- Eloquent determines the foreign key name by examining the name of the relationship method and suffixing the method name with `_id`. So, in this case, Eloquent assumes that the `Phone` model has a `user_id` column. However, if the foreign key on the `Phone` model is not `user_id`, you may pass a custom key name as the second argument to the `belongsTo` method: -->
Eloquent는 관계 메서드명을 분석해서 해당 외래 키명을 결정합니다. 즉, 메서드명에 `_id`를 붙여서 외래 키명으로 간주합니다. 위 예제에서도 `Phone` 모델에 `user_id` 컬럼이 있을 것으로 예상합니다. 만약 `Phone` 모델의 외래 키명이 `user_id`가 아니라면, `belongsTo`의 두 번째 인수로 원하는 외래 키명을 지정할 수 있습니다.

```
/**
 * Get the user that owns the phone.
 */
public function user()
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

<!-- If the parent model does not use `id` as its primary key, or you wish to find the associated model using a different column, you may pass a third argument to the `belongsTo` method specifying the parent table's custom key: -->
부모 모델이 `id` 외의 컬럼을 프라이머리 키로 사용하고 있거나, 관계의 대상 모델을 찾는 칼럼을 변경하고 싶은 경우, `belongsTo` 메서드의 세 번째 인수로 부모 테이블의 키 컬럼명을 지정할 수 있습니다.

```
/**
 * Get the user that owns the phone.
 */
public function user()
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a name="one-to-many"></a>
<!-- ### One To Many -->
### One To Many

<!-- A one-to-many relationship is used to define relationships where a single model is the parent to one or more child models. For example, a blog post may have an infinite number of comments. Like all other Eloquent relationships, one-to-many relationships are defined by defining a method on your Eloquent model: -->
일대다 관계는 한 모델이 여러 자식 모델을 소유하는 구조를 정의할 때 사용합니다. 예를 들어, 하나의 블로그 게시글(Post)은 여러 개의 댓글(Comment)을 가질 수 있습니다. 다른 Eloquent 관계처럼, 일대다 관계 역시 모델에서 메서드를 정의하는 방식으로 만들 수 있습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * Get the comments for the blog post.
     */
    public function comments()
    {
        return $this->hasMany(Comment::class);
    }
}
```

<!-- Remember, Eloquent will automatically determine the proper foreign key column for the `Comment` model. By convention, Eloquent will take the "snake case" name of the parent model and suffix it with `_id`. So, in this example, Eloquent will assume the foreign key column on the `Comment` model is `post_id`. -->
Eloquent는 자동으로 `Comment` 모델의 외래 키 컬럼명을 결정합니다. 관례적으로, 부모 모델명을 스네이크 케이스(snake_case)로 변환한 뒤 `_id`를 붙여서 외래 키명으로 사용합니다. 위 예제의 경우, `Comment` 모델의 외래 키 컬럼은 `post_id`로 간주합니다.

<!-- Once the relationship method has been defined, we can access the [collection](/docs/9.x/eloquent-collections) of related comments by accessing the `comments` property. Remember, since Eloquent provides "dynamic relationship properties", we can access relationship methods as if they were defined as properties on the model: -->
관계 메서드를 정의한 후, 관련 댓글들을 [collection](/docs/9.x/eloquent-collections) 형태로 `comments` 프로퍼티에 접근하여 조회할 수 있습니다. 앞에서 언급한 동적 관계 프로퍼티를 활용하면, 마치 속성처럼 사용할 수 있습니다.

```
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    //
}
```

<!-- Since all relationships also serve as query builders, you may add further constraints to the relationship query by calling the `comments` method and continuing to chain conditions onto the query: -->
관계도 쿼리 빌더의 역할을 하므로, `comments` 메서드에 쿼리 조건을 추가하여 더 세밀하게 결과를 제어할 수도 있습니다.

```
$comment = Post::find(1)->comments()
                    ->where('title', 'foo')
                    ->first();
```

<!-- Like the `hasOne` method, you may also override the foreign and local keys by passing additional arguments to the `hasMany` method: -->
`hasOne`과 마찬가지로, `hasMany` 메서드에도 두 번째, 세 번째 인수로 외래 키와 로컬 키를 직접 지정해서 사용할 수 있습니다.

```
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="one-to-many-inverse"></a>
<!-- ### One To Many (Inverse) / Belongs To -->
### One To Many (Inverse) / Belongs To

<!-- Now that we can access all of a post's comments, let's define a relationship to allow a comment to access its parent post. To define the inverse of a `hasMany` relationship, define a relationship method on the child model which calls the `belongsTo` method: -->
게시글의 댓글들을 모두 조회할 수 있게 되었으니, 이제는 댓글에서 자신의 부모 게시글에 접근하는 관계도 정의해 보겠습니다. `hasMany` 관계의 역방향은 자식 모델에서 `belongsTo` 메서드를 호출해 사용하는 방식으로 정의합니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Comment extends Model
{
    /**
     * Get the post that owns the comment.
     */
    public function post()
    {
        return $this->belongsTo(Post::class);
    }
}
```

<!-- Once the relationship has been defined, we can retrieve a comment's parent post by accessing the `post` "dynamic relationship property": -->
관계가 정의되면, `post`라는 동적 관계 프로퍼티를 이용해 해당 댓글의 소유 게시글을 조회할 수 있습니다.

```
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

<!-- In the example above, Eloquent will attempt to find a `Post` model that has an `id` which matches the `post_id` column on the `Comment` model. -->
위 예제에서 Eloquent는 `Comment` 모델의 `post_id` 값과 일치하는 `Post` 모델의 `id` 값을 찾아 반환합니다.

<!-- Eloquent determines the default foreign key name by examining the name of the relationship method and suffixing the method name with a `_` followed by the name of the parent model's primary key column. So, in this example, Eloquent will assume the `Post` model's foreign key on the `comments` table is `post_id`. -->
Eloquent는 관계 메서드명을 기반으로 기본 외래 키명을 결정합니다. 메서드명 다음에 `_`와 부모 모델 프라이머리 키명을 붙인 형태가 됩니다. 위 예제라면 `comments` 테이블에 대한 `Post` 모델의 외래 키가 `post_id`라고 간주합니다.

<!-- However, if the foreign key for your relationship does not follow these conventions, you may pass a custom foreign key name as the second argument to the `belongsTo` method: -->
만약 여러분의 관계에서 외래 키가 이런 관례를 따르지 않는다면, `belongsTo` 메서드의 두 번째 인수로 원하는 외래 키명을 지정할 수 있습니다.

```
/**
 * Get the post that owns the comment.
 */
public function post()
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

<!-- If your parent model does not use `id` as its primary key, or you wish to find the associated model using a different column, you may pass a third argument to the `belongsTo` method specifying your parent table's custom key: -->
마찬가지로, 부모 모델이 `id` 이외의 컬럼을 프라이머리 키로 사용하거나, 다른 컬럼으로 연관시키고 싶은 경우, `belongsTo` 메서드의 세 번째 인수로 부모 테이블의 프라이머리 키명을 지정할 수 있습니다.

```
/**
 * Get the post that owns the comment.
 */
public function post()
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
<!-- #### Default Models -->
#### Default Models

<!-- The `belongsTo`, `hasOne`, `hasOneThrough`, and `morphOne` relationships allow you to define a default model that will be returned if the given relationship is `null`. This pattern is often referred to as the [Null Object pattern](https://en.wikipedia.org/wiki/Null_Object_pattern) and can help remove conditional checks in your code. In the following example, the `user` relation will return an empty `App\Models\User` model if no user is attached to the `Post` model: -->
`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 관계에서는 관계가 `null`일 때 반환할 기본 모델(default model)을 정의할 수 있습니다. 이런 패턴은 종종 [Null Object pattern](https://en.wikipedia.org/wiki/Null_Object_pattern)이라고도 하며, 코드에서 조건문을 줄여주어 더욱 간결하게 만들어줍니다. 아래 예제에서는 `Post` 모델에 연결된 사용자가 없을 경우, `user` 관계는 빈 `App\Models\User` 모델을 반환합니다.

```
/**
 * Get the author of the post.
 */
public function user()
{
    return $this->belongsTo(User::class)->withDefault();
}
```

<!-- To populate the default model with attributes, you may pass an array or closure to the `withDefault` method: -->
기본 모델에 속성값을 채워주고 싶다면, `withDefault` 메서드에 배열이나 클로저를 전달하면 됩니다.

```
/**
 * Get the author of the post.
 */
public function user()
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

/**
 * Get the author of the post.
 */
public function user()
{
    return $this->belongsTo(User::class)->withDefault(function ($user, $post) {
        $user->name = 'Guest Author';
    });
}
```

<a name="querying-belongs-to-relationships"></a>
<!-- #### Querying Belongs To Relationships -->
#### Querying Belongs To Relationships

<!-- When querying for the children of a "belongs to" relationship, you may manually build the `where` clause to retrieve the corresponding Eloquent models: -->
"belongs to" 관계의 자식 모델들을 쿼리할 때, `where` 절을 직접 작성해서 관련된 Eloquent 모델을 조회할 수 있습니다.

```
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

<!-- However, you may find it more convenient to use the `whereBelongsTo` method, which will automatically determine the proper relationship and foreign key for the given model: -->
하지만, `whereBelongsTo` 메서드를 활용하면 적절한 관계 및 외래 키를 프레임워크에서 자동으로 결정하므로 더욱 편리합니다.

```
$posts = Post::whereBelongsTo($user)->get();
```

<!-- You may also provide a [collection](/docs/9.x/eloquent-collections) instance to the `whereBelongsTo` method. When doing so, Laravel will retrieve models that belong to any of the parent models within the collection: -->
또한, `whereBelongsTo` 메서드에 [collection](/docs/9.x/eloquent-collections) 인스턴스를 넘길 수도 있습니다. 이 경우 컬렉션 내의 부모 모델들 중 어느 것과 연관된 모델이든 모두 조회할 수 있습니다.

```
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

<!-- By default, Laravel will determine the relationship associated with the given model based on the class name of the model; however, you may specify the relationship name manually by providing it as the second argument to the `whereBelongsTo` method: -->
기본적으로 Laravel은 전달된 모델의 클래스명을 기준으로 관계명을 판단하지만, `whereBelongsTo` 메서드의 두 번째 인수로 직접 관계명을 지정할 수도 있습니다.

```
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
<!-- ### Has One Of Many -->
### Has One Of Many

<!-- Sometimes a model may have many related models, yet you want to easily retrieve the "latest" or "oldest" related model of the relationship. For example, a `User` model may be related to many `Order` models, but you want to define a convenient way to interact with the most recent order the user has placed. You may accomplish this using the `hasOne` relationship type combined with the `ofMany` methods: -->
어떤 모델이 여러 연관 모델을 가질 수 있지만, 이 중 "가장 최근" 또는 "가장 오래된" 관계 모델 하나만을 쉽고 빠르게 조회하고 싶을 때가 있습니다. 예를 들어, `User` 모델은 여러 개의 `Order` 모델과 연관될 수 있지만, 그 중 사용자가 가장 최근에 주문한 한 건만 빠르게 조회하고 싶은 경우가 있습니다. 이런 상황에서는 `hasOne` 관계에 `ofMany` 관련 메서드를 조합해서 사용할 수 있습니다.

```php
/**
 * Get the user's most recent order.
 */
public function latestOrder()
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

<!-- Likewise, you may define a method to retrieve the "oldest", or first, related model of a relationship: -->
마찬가지로, "가장 오래된" 혹은 첫 번째 연관 모델을 조회하는 메서드도 정의할 수 있습니다.

```php
/**
 * Get the user's oldest order.
 */
public function oldestOrder()
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

<!-- By default, the `latestOfMany` and `oldestOfMany` methods will retrieve the latest or oldest related model based on the model's primary key, which must be sortable. However, sometimes you may wish to retrieve a single model from a larger relationship using a different sorting criteria. -->
기본적으로 `latestOfMany` 및 `oldestOfMany` 메서드는 프라이머리 키를 기준으로 내림차순 또는 오름차순으로 정렬하여 가장 최신 또는 가장 오래된 연관 모델을 찾습니다(프라이머리 키가 정렬 가능한 데이터여야 합니다). 하지만, 더 복잡한 정렬 기준으로 원하는 단일 모델을 선택해야 할 경우가 있습니다.

<!-- For example, using the `ofMany` method, you may retrieve the user's most expensive order. The `ofMany` method accepts the sortable column as its first argument and which aggregate function (`min` or `max`) to apply when querying for the related model: -->
예를 들어, `ofMany` 메서드를 사용하여 사용자가 주문한 금액이 가장 큰 주문을 조회할 수도 있습니다. `ofMany`의 첫 번째 인수는 정렬에 사용할 컬럼, 두 번째 인수는 사용할 집계 함수(`min` 또는 `max`)를 의미합니다.

```php
/**
 * Get the user's largest order.
 */
public function largestOrder()
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```

> [!WARNING]
> PostgreSQL에서는 UUID 칼럼에 대해 `MAX` 함수를 실행하는 것을 지원하지 않으므로, PostgreSQL UUID 칼럼과 one-of-many 관계를 조합하여 사용하는 것은 현재 불가능합니다.

<a name="advanced-has-one-of-many-relationships"></a>
<!-- #### Advanced Has One Of Many Relationships -->
#### Advanced Has One Of Many Relationships

<!-- It is possible to construct more advanced "has one of many" relationships. For example, a `Product` model may have many associated `Price` models that are retained in the system even after new pricing is published. In addition, new pricing data for the product may be able to be published in advance to take effect at a future date via a `published_at` column. -->
좀 더 복잡한 "has one of many" 관계도 정의할 수 있습니다. 예를 들어, `Product` 모델이 여러 개의 `Price` 모델과 연관되어 있고, 새로운 가격은 미리 등록해서 지정한 `published_at` 날짜가 되어야 효력이 발생하도록 되어 있다고 가정해봅시다. 즉, 미래의 효력이 발생할 가격도 미리 저장해둘 수 있습니다.

<!-- So, in summary, we need to retrieve the latest published pricing where the published date is not in the future. In addition, if two prices have the same published date, we will prefer the price with the greatest ID. To accomplish this, we must pass an array to the `ofMany` method that contains the sortable columns which determine the latest price. In addition, a closure will be provided as the second argument to the `ofMany` method. This closure will be responsible for adding additional publish date constraints to the relationship query: -->
이 경우, 발행일이 미래가 아닌 가장 최근의 가격 정보만을 조회해야 하고, 만약 발행일이 같은 가격이 여러 개라면 id가 가장 높은(즉, 가장 마지막에 입력된) 가격을 선택하고 싶습니다. 이런 경우에는 `ofMany` 메서드에 가장 최신 가격을 결정하는 정렬 기준 컬럼들을 배열로 넘기고, `ofMany` 메서드의 두 번째 인수로 클로저를 전달해 추가적인 발행일 조건을 적용할 수 있습니다.

```php
/**
 * Get the current pricing for the product.
 */
public function currentPricing()
{
    return $this->hasOne(Price::class)->ofMany([
        'published_at' => 'max',
        'id' => 'max',
    ], function ($query) {
        $query->where('published_at', '<', now());
    });
}
```

<a name="has-one-through"></a>
<!-- ### Has One Through -->
### Has One Through

<!-- The "has-one-through" relationship defines a one-to-one relationship with another model. However, this relationship indicates that the declaring model can be matched with one instance of another model by proceeding _through_ a third model. -->
"has-one-through" 관계는 한 모델이, 중간에 다른 모델을 경유하여, 마지막 외부 모델과 일대일(one-to-one) 연결되는 구조입니다. 즉, 관계 선언을 한 모델이 중간 모델을 _통해_ 다른 한 모델과 연관됩니다.

<!-- For example, in a vehicle repair shop application, each `Mechanic` model may be associated with one `Car` model, and each `Car` model may be associated with one `Owner` model. While the mechanic and the owner have no direct relationship within the database, the mechanic can access the owner _through_ the `Car` model. Let's look at the tables necessary to define this relationship: -->
예를 들어, 정비소(차량수리점) 애플리케이션에서 각각의 `Mechanic`(정비사) 모델은 하나의 `Car`(차) 모델과 연결되어 있고, 각각의 `Car` 모델은 하나의 `Owner`(차주) 모델과 연결되어 있다고 합시다. 이 경우 정비사와 차주는 데이터베이스상 직접 연결되어 있지 않지만, 정비사는 `Car` 모델을 _경유해서_ 차주에게 접근할 수 있습니다. 필요한 테이블 구조는 다음과 같습니다.

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
테이블 구조를 확인했다면, 이제 `Mechanic` 모델에 관계를 정의해보겠습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Mechanic extends Model
{
    /**
     * Get the car's owner.
     */
    public function carOwner()
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```

<!-- The first argument passed to the `hasOneThrough` method is the name of the final model we wish to access, while the second argument is the name of the intermediate model. -->
`hasOneThrough`의 첫 번째 인수는 접근하고자 하는 최종(target) 모델명이며, 두 번째 인수는 중간 모델명입니다.

<!-- Or, if the relevant relationships have already been defined on all of the models involved in the relationship, you may fluently define a "has-one-through" relationship by invoking the `through` method and supplying the names of those relationships. For example, if the `Mechanic` model has a `cars` relationship and the `Car` model has an `owner` relationship, you may define a "has-one-through" relationship connecting the mechanic and the owner like so: -->
또는, 관계에 참여하는 모든 모델에 해당 관계가 이미 정의되어 있을 경우, `through` 메서드를 사용하여 관계명을 문자열로 지정해 좀 더 선언적으로 "has-one-through" 관계를 정의할 수 있습니다. 예를 들어, `Mechanic` 모델에 `cars` 관계가, `Car` 모델에 `owner` 관계가 정의되어 있으면 아래처럼 사용할 수 있습니다.

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
관계 쿼리를 수행할 때는 Eloquent의 일반적인 외래 키 명명 규칙이 적용됩니다. 만약 관계에 사용할 키를 직접 지정하고 싶다면, `hasOneThrough`의 세 번째와 네 번째 인수로 각각 중간 모델의 외래 키와 최종(target) 모델의 외래 키명을 넘기면 됩니다. 다섯 번째 인수는 원래(로컬) 키, 여섯 번째 인수는 중간 모델의 로컬 키입니다.

```
class Mechanic extends Model
{
    /**
     * Get the car's owner.
     */
    public function carOwner()
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
앞서 설명한 것처럼, 관계에 참여하는 모든 모델에 해당 관계가 정의되어 있다면, `through` 메서드와 관계명 지정으로 키 명명 규칙을 간결하게 재사용할 수 있습니다.

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
"has-many-through" 관계는 중간 관계를 통해 멀리 떨어진 연관 데이터를 간편하게 조회하는 방법을 제공합니다. 예를 들어, [Laravel Vapor](https://vapor.laravel.com)와 같은 배포 플랫폼을 개발한다고 가정해봅시다. `Project` 모델은 중간에 `Environment` 모델을 경유하여 여러 개의 `Deployment`(배포) 모델에 접근할 수 있습니다. 이 구조를 활용하면 하나의 프로젝트에 대한 모든 배포 내역을 손쉽게 모을 수 있습니다. 필요한 테이블은 아래와 같습니다.

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
테이블 구조를 확인했다면, 관계를 `Project` 모델에 다음과 같이 정의할 수 있습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Project extends Model
{
    /**
     * Get all of the deployments for the project.
     */
    public function deployments()
    {
        return $this->hasManyThrough(Deployment::class, Environment::class);
    }
}
```

<!-- The first argument passed to the `hasManyThrough` method is the name of the final model we wish to access, while the second argument is the name of the intermediate model. -->
`hasManyThrough`의 첫 번째 인수는 최종적으로 접근하려는 모델명, 두 번째 인수는 중간 모델명입니다.

<!-- Or, if the relevant relationships have already been defined on all of the models involved in the relationship, you may fluently define a "has-many-through" relationship by invoking the `through` method and supplying the names of those relationships. For example, if the `Project` model has a `environments` relationship and the `Environment` model has a `deployments` relationship, you may define a "has-many-through" relationship connecting the project and the deployments like so: -->
또는, 관계에 참여하는 모든 모델에 관계가 이미 정의되어 있다면, `through` 메서드와 관계명을 사용해 더 간결하게 선언할 수도 있습니다. 예를 들어, `Project` 모델에 `environments` 관계가 있고 `Environment` 모델에 `deployments` 관계가 있다면, 다음처럼 프로젝트와 배포를 연결하는 "has-many-through" 관계를 정의할 수 있습니다.

```php
// String based syntax...
return $this->through('environments')->has('deployments');

// Dynamic syntax...
return $this->throughEnvironments()->hasDeployments();
```

<!-- Though the `Deployment` model's table does not contain a `project_id` column, the `hasManyThrough` relation provides access to a project's deployments via `$project->deployments`. To retrieve these models, Eloquent inspects the `project_id` column on the intermediate `Environment` model's table. After finding the relevant environment IDs, they are used to query the `Deployment` model's table. -->
`Deployment` 모델 테이블에는 `project_id` 컬럼이 직접 있지 않지만, `hasManyThrough` 관계 덕분에 `$project->deployments`처럼 프로젝트의 모든 배포 정보를 간편하게 조회할 수 있습니다. 내부적으로 Eloquent는 중간 모델인 `Environment` 모델 테이블의 `project_id` 칼럼을 먼저 조회해 관련 환경의 id를 찾고, 그 id들을 이용해 `Deployment` 모델 테이블에서 데이터를 가져옵니다.

<a name="has-many-through-key-conventions"></a>

<!-- #### Key Conventions -->
#### Key Conventions

<!-- Typical Eloquent foreign key conventions will be used when performing the relationship's queries. If you would like to customize the keys of the relationship, you may pass them as the third and fourth arguments to the `hasManyThrough` method. The third argument is the name of the foreign key on the intermediate model. The fourth argument is the name of the foreign key on the final model. The fifth argument is the local key, while the sixth argument is the local key of the intermediate model: -->
관계 쿼리를 수행할 때는 일반적인 Eloquent 외래 키 규칙이 사용됩니다. 관계의 키를 커스터마이즈하고 싶다면, `hasManyThrough` 메서드의 세 번째와 네 번째 인수로 지정할 수 있습니다. 세 번째 인수는 중간 모델에 있는 외래 키의 이름이고, 네 번째 인수는 마지막 모델에 있는 외래 키의 이름입니다. 다섯 번째 인수는 로컬 키이고, 여섯 번째 인수는 중간 모델의 로컬 키입니다.

```
class Project extends Model
{
    public function deployments()
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
또는, 앞서 설명한 것처럼, 관계에 참여하는 모든 모델에서 필요한 관계가 이미 정의되어 있다면 `through` 메서드에 해당 관계들의 이름을 전달하여 "has-many-through" 관계를 더욱 유연하게 정의할 수 있습니다. 이 방법의 장점은 이미 기존 관계에 정의된 키 규칙을 재사용할 수 있다는 점입니다.

```php
// String based syntax...
return $this->through('environments')->has('deployments');

// Dynamic syntax...
return $this->throughEnvironments()->hasDeployments();
```

<a name="many-to-many"></a>
<!-- ## Many To Many Relationships -->
## Many To Many Relationships

<!-- Many-to-many relations are slightly more complicated than `hasOne` and `hasMany` relationships. An example of a many-to-many relationship is a user that has many roles and those roles are also shared by other users in the application. For example, a user may be assigned the role of "Author" and "Editor"; however, those roles may also be assigned to other users as well. So, a user has many roles and a role has many users. -->
다대다(Many-to-many) 관계는 `hasOne`이나 `hasMany` 관계보다 약간 더 복잡합니다. 예를 들어, 하나의 사용자가 여러 역할(Role)을 가질 수 있고, 해당 역할들은 다른 사용자와도 공유될 수 있습니다. 즉, 한 사용자가 "Author"와 "Editor" 역할을 부여받을 수 있고, 이 역할들은 다른 사용자에게도 부여될 수 있습니다. 따라서 하나의 사용자는 여러 역할을, 하나의 역할은 여러 사용자를 가집니다.

<a name="many-to-many-table-structure"></a>
<!-- #### Table Structure -->
#### Table Structure

<!-- To define this relationship, three database tables are needed: `users`, `roles`, and `role_user`. The `role_user` table is derived from the alphabetical order of the related model names and contains `user_id` and `role_id` columns. This table is used as an intermediate table linking the users and roles. -->
이 관계를 정의하려면 `users`, `roles`, `role_user`의 3개 데이터베이스 테이블이 필요합니다. `role_user` 테이블은 관련 모델 이름의 알파벳 순으로 만들어지며, `user_id`와 `role_id` 컬럼을 가집니다. 이 테이블은 사용자와 역할을 연결하는 중간 테이블로 사용됩니다.

<!-- Remember, since a role can belong to many users, we cannot simply place a `user_id` column on the `roles` table. This would mean that a role could only belong to a single user. In order to provide support for roles being assigned to multiple users, the `role_user` table is needed. We can summarize the relationship's table structure like so: -->
역할이 여러 사용자에게 속할 수 있으므로, `roles` 테이블에 단순히 `user_id` 컬럼을 추가해서는 안됩니다. 그렇게 하면 한 역할이 오직 한 사용자에게만 속하는 의미가 되기 때문입니다. 여러 사용자에게 역할을 할당하려면 반드시 `role_user` 중간 테이블이 필요합니다. 관계의 테이블 구조를 요약하면 다음과 같습니다.

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
다대다 관계는 `belongsToMany` 메서드의 결과를 반환하는 메서드를 작성하여 정의합니다. `belongsToMany` 메서드는 애플리케이션의 모든 Eloquent 모델이 상속 받는 `Illuminate\Database\Eloquent\Model` 기본 클래스에서 제공됩니다. 예를 들어, `User` 모델에 `roles` 메서드를 정의할 수 있습니다. 이 메서드의 첫 번째 인수는 연결할 모델 클래스의 이름입니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The roles that belong to the user.
     */
    public function roles()
    {
        return $this->belongsToMany(Role::class);
    }
}
```

<!-- Once the relationship is defined, you may access the user's roles using the `roles` dynamic relationship property: -->
관계를 정의한 후에는, `roles` 동적 관계 속성을 사용해 사용자의 역할에 접근할 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    //
}
```

<!-- Since all relationships also serve as query builders, you may add further constraints to the relationship query by calling the `roles` method and continuing to chain conditions onto the query: -->
모든 관계는 쿼리 빌더 역할도 하므로, `roles` 메서드를 호출하고 조건을 체이닝해서 추가 제약 조건을 쿼리에 붙일 수 있습니다.

```
$roles = User::find(1)->roles()->orderBy('name')->get();
```

<!-- To determine the table name of the relationship's intermediate table, Eloquent will join the two related model names in alphabetical order. However, you are free to override this convention. You may do so by passing a second argument to the `belongsToMany` method: -->
관계의 중간 테이블명을 결정할 때, Eloquent는 두 관련 모델 이름을 알파벳 순으로 조합합니다. 하지만 이 규칙을 직접 오버라이드할 수 있습니다. `belongsToMany`의 두 번째 인수로 테이블명을 지정하면 됩니다.

```
return $this->belongsToMany(Role::class, 'role_user');
```

<!-- In addition to customizing the name of the intermediate table, you may also customize the column names of the keys on the table by passing additional arguments to the `belongsToMany` method. The third argument is the foreign key name of the model on which you are defining the relationship, while the fourth argument is the foreign key name of the model that you are joining to: -->
중간 테이블의 이름뿐만이 아니라, `belongsToMany` 메서드에 추가 인수를 전달해 테이블의 키 컬럼명 역시 지정할 수 있습니다. 세 번째 인수는 현재 모델의 외래 키, 네 번째 인수는 조인할 모델의 외래 키입니다.

```
return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');
```

<a name="many-to-many-defining-the-inverse-of-the-relationship"></a>
<!-- #### Defining The Inverse Of The Relationship -->
#### Defining The Inverse Of The Relationship

<!-- To define the "inverse" of a many-to-many relationship, you should define a method on the related model which also returns the result of the `belongsToMany` method. To complete our user / role example, let's define the `users` method on the `Role` model: -->
다대다 관계의 "반대"를 정의하려면, 관련 모델에도 `belongsToMany` 메서드를 반환하는 메서드를 정의해야 합니다. 사용자/역할 예시를 완성하기 위해 `Role` 모델에 `users` 메서드를 정의해봅시다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Role extends Model
{
    /**
     * The users that belong to the role.
     */
    public function users()
    {
        return $this->belongsToMany(User::class);
    }
}
```

<!-- As you can see, the relationship is defined exactly the same as its `User` model counterpart with the exception of referencing the `App\Models\User` model. Since we're reusing the `belongsToMany` method, all of the usual table and key customization options are available when defining the "inverse" of many-to-many relationships. -->
보시다시피, 관계 정의 방식은 `User` 모델의 경우와 거의 동일하며, 단지 `App\Models\User`을 참조한다는 점만 다릅니다. `belongsToMany`를 재사용하기 때문에, 다대다 관계의 "반대"를 정의할 때도 테이블과 키의 커스터마이징 옵션을 모두 사용할 수 있습니다.

<a name="retrieving-intermediate-table-columns"></a>
<!-- ### Retrieving Intermediate Table Columns -->
### Retrieving Intermediate Table Columns

<!-- As you have already learned, working with many-to-many relations requires the presence of an intermediate table. Eloquent provides some very helpful ways of interacting with this table. For example, let's assume our `User` model has many `Role` models that it is related to. After accessing this relationship, we may access the intermediate table using the `pivot` attribute on the models: -->
이미 살펴봤듯, 다대다 관계를 사용하려면 중간 테이블이 필요합니다. Eloquent는 이 중간 테이블을 다루기 위한 다양한 방법을 제공합니다. 예를 들어, `User` 모델이 여러 `Role` 모델과 연결되어 있다면, 이 관계를 통해 중간 테이블의 값에 `pivot` 속성으로 접근할 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    echo $role->pivot->created_at;
}
```

<!-- Notice that each `Role` model we retrieve is automatically assigned a `pivot` attribute. This attribute contains a model representing the intermediate table. -->
조회된 각 `Role` 모델에는 자동으로 `pivot` 속성이 할당됩니다. 이 속성은 중간 테이블을 나타내는 모델을 포함합니다.

<!-- By default, only the model keys will be present on the `pivot` model. If your intermediate table contains extra attributes, you must specify them when defining the relationship: -->
기본적으로 `pivot` 모델에는 키 컬럼만 포함됩니다. 만약 중간 테이블에 추가 속성이 있다면, 관계를 정의할 때 그 속성들을 명시해주어야 합니다.

```
return $this->belongsToMany(Role::class)->withPivot('active', 'created_by');
```

<!-- If you would like your intermediate table to have `created_at` and `updated_at` timestamps that are automatically maintained by Eloquent, call the `withTimestamps` method when defining the relationship: -->
중간 테이블에 `created_at`과 `updated_at` 타임스탬프가 존재하고, Eloquent가 이를 자동으로 관리하게 하려면 관계 정의 시 `withTimestamps` 메서드를 호출하면 됩니다.

```
return $this->belongsToMany(Role::class)->withTimestamps();
```

> [!WARNING]
> Eloquent가 자동으로 관리하는 타임스탬프를 사용하는 중간 테이블에는 반드시 `created_at`과 `updated_at` 컬럼이 모두 존재해야 합니다.

<a name="customizing-the-pivot-attribute-name"></a>
<!-- #### Customizing The `pivot` Attribute Name -->
#### Customizing The `pivot` Attribute Name

<!-- As noted previously, attributes from the intermediate table may be accessed on models via the `pivot` attribute. However, you are free to customize the name of this attribute to better reflect its purpose within your application. -->
앞에서 언급했듯, 중간 테이블의 속성은 모델에서 `pivot` 속성으로 접근 가능합니다. 그러나 필요하다면, 이 속성 이름을 애플리케이션에 더 적합한 이름으로 변경할 수 있습니다.

<!-- For example, if your application contains users that may subscribe to podcasts, you likely have a many-to-many relationship between users and podcasts. If this is the case, you may wish to rename your intermediate table attribute to `subscription` instead of `pivot`. This can be done using the `as` method when defining the relationship: -->
예를 들어, 사용자가 팟캐스트를 구독(subscribe)할 수 있는 구조라면, 사용자와 팟캐스트 간의 다대다 관계에서 중간 테이블 속성을 `pivot` 대신 `subscription`처럼 의미 있는 이름으로 정의하고 싶을 수 있습니다. 이를 위해 관계 정의 시 `as` 메서드를 활용할 수 있습니다.

```
return $this->belongsToMany(Podcast::class)
                ->as('subscription')
                ->withTimestamps();
```

<!-- Once the custom intermediate table attribute has been specified, you may access the intermediate table data using the customized name: -->
이렇게 커스텀 중간 테이블 속성을 지정하면, 해당 이름으로 중간 테이블 데이터를 조회할 수 있습니다.

```
$users = User::with('podcasts')->get();

foreach ($users->flatMap->podcasts as $podcast) {
    echo $podcast->subscription->created_at;
}
```

<a name="filtering-queries-via-intermediate-table-columns"></a>
<!-- ### Filtering Queries Via Intermediate Table Columns -->
### Filtering Queries Via Intermediate Table Columns

<!-- You can also filter the results returned by `belongsToMany` relationship queries using the `wherePivot`, `wherePivotIn`, `wherePivotNotIn`, `wherePivotBetween`, `wherePivotNotBetween`, `wherePivotNull`, and `wherePivotNotNull` methods when defining the relationship: -->
`belongsToMany` 관계 쿼리에 대해 `wherePivot`, `wherePivotIn`, `wherePivotNotIn`, `wherePivotBetween`, `wherePivotNotBetween`, `wherePivotNull`, `wherePivotNotNull` 메서드를 사용하여, 중간 테이블 컬럼의 값을 기준으로 결과를 필터링할 수 있습니다.

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

<a name="ordering-queries-via-intermediate-table-columns"></a>
<!-- ### Ordering Queries Via Intermediate Table Columns -->
### Ordering Queries Via Intermediate Table Columns

<!-- You can order the results returned by `belongsToMany` relationship queries using the `orderByPivot` method. In the following example, we will retrieve all of the latest badges for the user: -->
`belongsToMany` 관계 쿼리의 반환 결과를 `orderByPivot` 메서드로 중간 테이블 컬럼 기준으로 정렬할 수 있습니다. 다음 예시에서는 사용자의 최신 배지를 조회합니다.

```
return $this->belongsToMany(Badge::class)
                ->where('rank', 'gold')
                ->orderByPivot('created_at', 'desc');
```

<a name="defining-custom-intermediate-table-models"></a>
<!-- ### Defining Custom Intermediate Table Models -->
### Defining Custom Intermediate Table Models

<!-- If you would like to define a custom model to represent the intermediate table of your many-to-many relationship, you may call the `using` method when defining the relationship. Custom pivot models give you the opportunity to define additional behavior on the pivot model, such as methods and casts. -->
다대다 관계의 중간 테이블을 나타내는 커스텀 모델을 정의하고 싶다면, 관계 정의 시 `using` 메서드를 사용할 수 있습니다. 커스텀 pivot 모델을 사용하면, 그 모델에 메서드나 속성 변환(casts) 등 추가 동작을 정의할 수 있습니다.

<!-- Custom many-to-many pivot models should extend the `Illuminate\Database\Eloquent\Relations\Pivot` class while custom polymorphic many-to-many pivot models should extend the `Illuminate\Database\Eloquent\Relations\MorphPivot` class. For example, we may define a `Role` model which uses a custom `RoleUser` pivot model: -->
커스텀 다대다 pivot 모델은 `Illuminate\Database\Eloquent\Relations\Pivot` 클래스를 상속해야 하며, 커스텀 다형 다대다(polimorphic many-to-many) pivot 모델은 `Illuminate\Database\Eloquent\Relations\MorphPivot` 클래스를 상속해야 합니다. 예를 들어, 커스텀 `RoleUser` pivot 모델을 사용하는 `Role` 모델을 정의할 수 있습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Role extends Model
{
    /**
     * The users that belong to the role.
     */
    public function users()
    {
        return $this->belongsToMany(User::class)->using(RoleUser::class);
    }
}
```

<!-- When defining the `RoleUser` model, you should extend the `Illuminate\Database\Eloquent\Relations\Pivot` class: -->
`RoleUser` 모델을 정의할 때에는 `Illuminate\Database\Eloquent\Relations\Pivot` 클래스를 반드시 상속해야 합니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Relations\Pivot;

class RoleUser extends Pivot
{
    //
}
```

> [!WARNING]
> Pivot 모델은 `SoftDeletes` 트레이트를 사용할 수 없습니다. Pivot 레코드를 소프트 삭제해야 한다면, pivot 모델을 실제 Eloquent 모델로 변환하는 것을 고려해보십시오.

<a name="custom-pivot-models-and-incrementing-ids"></a>
<!-- #### Custom Pivot Models And Incrementing IDs -->
#### Custom Pivot Models And Incrementing IDs

<!-- If you have defined a many-to-many relationship that uses a custom pivot model, and that pivot model has an auto-incrementing primary key, you should ensure your custom pivot model class defines an `incrementing` property that is set to `true`. -->
만약 커스텀 pivot 모델을 사용하는 다대다 관계를 정의했고, 해당 pivot 모델에 자동 증가(autoincrement) 기본 키가 있다면, 해당 pivot 모델 클래스에서 `incrementing` 속성이 `true`로 설정되어 있어야 합니다.

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
다형(Polymorphic) 관계를 사용하면 자식 모델이 여러 타입의 모델에 하나의 연관으로 속할 수 있습니다. 예를 들어, 사용자가 블로그 게시글과 동영상을 공유하는 애플리케이션을 만든다고 가정해봅시다. 이런 경우, `Comment` 모델이 `Post` 모델과 `Video` 모델 모두에 속할 수 있습니다.

<a name="one-to-one-polymorphic-relations"></a>
<!-- ### One To One (Polymorphic) -->
### One To One (Polymorphic)

<a name="one-to-one-polymorphic-table-structure"></a>
<!-- #### Table Structure -->
#### Table Structure

<!-- A one-to-one polymorphic relation is similar to a typical one-to-one relation; however, the child model can belong to more than one type of model using a single association. For example, a blog `Post` and a `User` may share a polymorphic relation to an `Image` model. Using a one-to-one polymorphic relation allows you to have a single table of unique images that may be associated with posts and users. First, let's examine the table structure: -->
일대일 다형 관계는 일반적인 일대일 관계와 비슷하지만, 한 자식 모델이 여러 타입의 모델과 하나의 연관을 가질 수 있다는 차이가 있습니다. 예를 들어, 블로그의 `Post`와 `User`가 모두 하나의 `Image` 모델과 다형 관계를 가질 수 있습니다. 일대일 다형 관계를 이용하면, 게시글이나 사용자에 연결될 수 있는 고유한 이미지들을 단일 테이블에 관리할 수 있습니다. 먼저, 테이블 구조를 살펴보겠습니다.

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
`images` 테이블에 있는 `imageable_id`와 `imageable_type` 컬럼에 주목하세요. `imageable_id` 컬럼에는 게시글이나 사용자의 ID가 저장되고, `imageable_type` 컬럼에는 부모 모델의 클래스명이 저장됩니다. `imageable` 관계에 접근할 때, Eloquent는 `imageable_type` 컬럼을 통해 어떤 "타입"의 부모 모델을 반환해야 할지 판단하게 됩니다. 이 경우, 컬럼 값은 `App\Models\Post` 또는 `App\Models\User` 중 하나가 됩니다.

<a name="one-to-one-polymorphic-model-structure"></a>
<!-- #### Model Structure -->
#### Model Structure

<!-- Next, let's examine the model definitions needed to build this relationship: -->
이제 이 관계를 구성하기 위해 필요한 모델 정의를 확인해봅시다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Image extends Model
{
    /**
     * Get the parent imageable model (user or post).
     */
    public function imageable()
    {
        return $this->morphTo();
    }
}

class Post extends Model
{
    /**
     * Get the post's image.
     */
    public function image()
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}

class User extends Model
{
    /**
     * Get the user's image.
     */
    public function image()
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}
```

<a name="one-to-one-polymorphic-retrieving-the-relationship"></a>
<!-- #### Retrieving The Relationship -->
#### Retrieving The Relationship

<!-- Once your database table and models are defined, you may access the relationships via your models. For example, to retrieve the image for a post, we can access the `image` dynamic relationship property: -->
데이터베이스 테이블과 모델이 준비되면, 모델을 통해 관계에 접근할 수 있습니다. 예를 들어, 게시글의 이미지를 가져오려면 `image` 동적 관계 속성을 사용하면 됩니다.

```
use App\Models\Post;

$post = Post::find(1);

$image = $post->image;
```

<!-- You may retrieve the parent of the polymorphic model by accessing the name of the method that performs the call to `morphTo`. In this case, that is the `imageable` method on the `Image` model. So, we will access that method as a dynamic relationship property: -->
다형 모델의 부모를 조회하려면, 내부적으로 `morphTo`를 호출하는 메서드의 이름을 동적 관계 속성으로 사용하면 됩니다. 이 예시에서는 `Image` 모델의 `imageable` 메서드입니다. 따라서 아래와 같이 접근할 수 있습니다.

```
use App\Models\Image;

$image = Image::find(1);

$imageable = $image->imageable;
```

<!-- The `imageable` relation on the `Image` model will return either a `Post` or `User` instance, depending on which type of model owns the image. -->
`Image` 모델의 `imageable` 관계는 해당 이미지를 소유하는 모델의 타입에 따라 `Post` 또는 `User` 인스턴스를 반환합니다.

<a name="morph-one-to-one-key-conventions"></a>
<!-- #### Key Conventions -->
#### Key Conventions

<!-- If necessary, you may specify the name of the "id" and "type" columns utilized by your polymorphic child model. If you do so, ensure that you always pass the name of the relationship as the first argument to the `morphTo` method. Typically, this value should match the method name, so you may use PHP's `__FUNCTION__` constant: -->
필요하다면, 다형 자식 모델이 사용하는 "id"와 "type" 컬럼명을 직접 지정할 수 있습니다. 이 경우에는 `morphTo` 메서드의 첫 번째 인수로 관계의 이름을 꼭 전달해야 합니다. 일반적으로 이 값은 메서드명과 동일하게 하면 되므로, PHP의 `__FUNCTION__` 상수를 사용할 수 있습니다.

```
/**
 * Get the model that the image belongs to.
 */
public function imageable()
{
    return $this->morphTo(__FUNCTION__, 'imageable_type', 'imageable_id');
}
```

<a name="one-to-many-polymorphic-relations"></a>
<!-- ### One To Many (Polymorphic) -->
### One To Many (Polymorphic)

<a name="one-to-many-polymorphic-table-structure"></a>
<!-- #### Table Structure -->
#### Table Structure

<!-- A one-to-many polymorphic relation is similar to a typical one-to-many relation; however, the child model can belong to more than one type of model using a single association. For example, imagine users of your application can "comment" on posts and videos. Using polymorphic relationships, you may use a single `comments` table to contain comments for both posts and videos. First, let's examine the table structure required to build this relationship: -->
일대다 다형 관계는 일반적인 일대다 관계와 유사하지만, 자식 모델이 하나의 연관을 통해 여러 타입의 모델에 속할 수 있다는 점이 다릅니다. 예를 들어, 애플리케이션에서 사용자가 게시글이나 동영상에 댓글(comment)을 남길 수 있다고 가정해봅시다. 이럴 때 다형 관계를 사용하면, `comments` 테이블 하나로 게시글과 동영상 모두에 달린 댓글을 관리할 수 있습니다. 먼저, 아래와 같은 테이블 구조가 필요합니다.

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
이제 이 관계를 구현하기 위한 모델 정의를 살펴보겠습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Comment extends Model
{
    /**
     * Get the parent commentable model (post or video).
     */
    public function commentable()
    {
        return $this->morphTo();
    }
}

class Post extends Model
{
    /**
     * Get all of the post's comments.
     */
    public function comments()
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}

class Video extends Model
{
    /**
     * Get all of the video's comments.
     */
    public function comments()
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}
```

<a name="one-to-many-polymorphic-retrieving-the-relationship"></a>
<!-- #### Retrieving The Relationship -->
#### Retrieving The Relationship

<!-- Once your database table and models are defined, you may access the relationships via your model's dynamic relationship properties. For example, to access all of the comments for a post, we can use the `comments` dynamic property: -->
데이터베이스 테이블과 모델이 준비되었다면, 동적 관계 속성을 통해 관계에 접근할 수 있습니다. 예를 들어, 게시글의 모든 댓글에 접근하려면 `comments` 동적 속성을 사용할 수 있습니다.

```
use App\Models\Post;

$post = Post::find(1);

foreach ($post->comments as $comment) {
    //
}
```

<!-- You may also retrieve the parent of a polymorphic child model by accessing the name of the method that performs the call to `morphTo`. In this case, that is the `commentable` method on the `Comment` model. So, we will access that method as a dynamic relationship property in order to access the comment's parent model: -->
다형 자식 모델의 부모를 조회할 때도, 내부적으로 `morphTo`를 호출하는 메서드명(여기서는 `Comment` 모델의 `commentable` 메서드)을 동적 속성으로 사용하면 됩니다.

```
use App\Models\Comment;

$comment = Comment::find(1);

$commentable = $comment->commentable;
```

<!-- The `commentable` relation on the `Comment` model will return either a `Post` or `Video` instance, depending on which type of model is the comment's parent. -->
`Comment` 모델의 `commentable` 관계는 해당 댓글의 부모 모델 타입에 따라 `Post` 또는 `Video` 인스턴스를 반환합니다.

<a name="one-of-many-polymorphic-relations"></a>
<!-- ### One Of Many (Polymorphic) -->
### One Of Many (Polymorphic)

<!-- Sometimes a model may have many related models, yet you want to easily retrieve the "latest" or "oldest" related model of the relationship. For example, a `User` model may be related to many `Image` models, but you want to define a convenient way to interact with the most recent image the user has uploaded. You may accomplish this using the `morphOne` relationship type combined with the `ofMany` methods: -->
때때로 하나의 모델이 여러 관련 모델을 가질 수 있지만, 그 중에서 "가장 최신" 또는 "가장 오래된" 하나의 관련 모델만 쉽게 가져오고 싶을 때가 있습니다. 예를 들어, `User` 모델이 여러 `Image` 모델과 연결되어 있지만, 사용자가 마지막으로 업로드한 이미지를 편하게 가져오고 싶을 수 있습니다. 이럴 때는 `morphOne` 관계와 `ofMany` 메서드를 조합해 구현할 수 있습니다.

```php
/**
 * Get the user's most recent image.
 */
public function latestImage()
{
    return $this->morphOne(Image::class, 'imageable')->latestOfMany();
}
```

<!-- Likewise, you may define a method to retrieve the "oldest", or first, related model of a relationship: -->
마찬가지로, 관계에서 "가장 오래된" 또는 첫 번째 관련 모델을 조회하는 메서드도 정의할 수 있습니다.

```php
/**
 * Get the user's oldest image.
 */
public function oldestImage()
{
    return $this->morphOne(Image::class, 'imageable')->oldestOfMany();
}
```

<!-- By default, the `latestOfMany` and `oldestOfMany` methods will retrieve the latest or oldest related model based on the model's primary key, which must be sortable. However, sometimes you may wish to retrieve a single model from a larger relationship using a different sorting criteria. -->
기본적으로 `latestOfMany`와 `oldestOfMany` 메서드는 해당 모델의 기본 키(정렬 가능한 값)를 기준으로 가장 최신 또는 가장 오래된 관련 모델을 가져옵니다. 하지만 때로는 더 큰 관계에서 다른 정렬 기준으로 단일 모델을 가져오고 싶을 수도 있습니다.

<!-- For example, using the `ofMany` method, you may retrieve the user's most "liked" image. The `ofMany` method accepts the sortable column as its first argument and which aggregate function (`min` or `max`) to apply when querying for the related model: -->
예를 들어, `ofMany` 메서드를 사용하면 사용자의 "좋아요"가 가장 많은 이미지를 가져올 수 있습니다. `ofMany` 메서드의 첫 번째 인수로 정렬 기준 컬럼을, 두 번째 인수로 사용할 집계 함수(예: `min` 또는 `max`)를 각각 전달하면 됩니다.

```php
/**
 * Get the user's most popular image.
 */
public function bestImage()
{
    return $this->morphOne(Image::class, 'imageable')->ofMany('likes', 'max');
}
```

> [!NOTE]
> 더 고급스러운 "다수 중 하나" 관계도 구성할 수 있습니다. 자세한 내용은 [has one of many documentation](#advanced-has-one-of-many-relationships)를 참고하세요.

<a name="many-to-many-polymorphic-relations"></a>
<!-- ### Many To Many (Polymorphic) -->
### Many To Many (Polymorphic)

<a name="many-to-many-polymorphic-table-structure"></a>
<!-- #### Table Structure -->
#### Table Structure

<!-- Many-to-many polymorphic relations are slightly more complicated than "morph one" and "morph many" relationships. For example, a `Post` model and `Video` model could share a polymorphic relation to a `Tag` model. Using a many-to-many polymorphic relation in this situation would allow your application to have a single table of unique tags that may be associated with posts or videos. First, let's examine the table structure required to build this relationship: -->
다형 다대다(many-to-many polymorphic) 관계는 "morph one"이나 "morph many" 관계보다 조금 더 복잡합니다. 예를 들어, `Post` 모델과 `Video` 모델이 모두 `Tag` 모델과 다형 다대다 관계를 맺을 수 있습니다. 이 구조를 사용하면, 게시글과 동영상 모두에 연결되는 고유한 태그를 하나의 테이블에서 관리할 수 있습니다. 아래는 이 관계를 구성하는 데 필요한 테이블 구조 예시입니다.

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
> 다형 다대다 관계를 본격적으로 살펴보기 전에, 일반적인 [many-to-many relationships](#many-to-many) 문서를 먼저 읽어보는 것이 도움이 될 수 있습니다.

<a name="many-to-many-polymorphic-model-structure"></a>

<!-- #### Model Structure -->
#### Model Structure

<!-- Next, we're ready to define the relationships on the models. The `Post` and `Video` models will both contain a `tags` method that calls the `morphToMany` method provided by the base Eloquent model class. -->
이제 모델에 관계를 정의할 준비가 되었습니다. `Post`와 `Video` 모델 모두 기본 Eloquent 모델 클래스에서 제공하는 `morphToMany` 메서드를 호출하는 `tags` 메서드를 포함하게 됩니다.

<!-- The `morphToMany` method accepts the name of the related model as well as the "relationship name". Based on the name we assigned to our intermediate table name and the keys it contains, we will refer to the relationship as "taggable": -->
`morphToMany` 메서드는 연관 모델의 이름과 "관계 이름"을 인자로 받습니다. 우리가 중간 테이블명과 키에 지정한 이름을 기준으로, 이 관계의 이름은 "taggable"로 참조합니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * Get all of the tags for the post.
     */
    public function tags()
    {
        return $this->morphToMany(Tag::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-defining-the-inverse-of-the-relationship"></a>
<!-- #### Defining The Inverse Of The Relationship -->
#### Defining The Inverse Of The Relationship

<!-- Next, on the `Tag` model, you should define a method for each of its possible parent models. So, in this example, we will define a `posts` method and a `videos` method. Both of these methods should return the result of the `morphedByMany` method. -->
다음으로, `Tag` 모델에서 각 부모 모델에 대한 메서드를 정의해야 합니다. 이 예시에서는 `posts` 메서드와 `videos` 메서드를 생성합니다. 이들 메서드는 모두 `morphedByMany` 메서드의 결과를 반환해야 합니다.

<!-- The `morphedByMany` method accepts the name of the related model as well as the "relationship name". Based on the name we assigned to our intermediate table name and the keys it contains, we will refer to the relationship as "taggable": -->
`morphedByMany` 메서드 역시 연관 모델 이름과 "관계 이름"을 인자로 받습니다. 우리가 중간 테이블명과 키에 지정한 이름을 기준으로, 이 관계의 이름 역시 "taggable"로 참조합니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Tag extends Model
{
    /**
     * Get all of the posts that are assigned this tag.
     */
    public function posts()
    {
        return $this->morphedByMany(Post::class, 'taggable');
    }

    /**
     * Get all of the videos that are assigned this tag.
     */
    public function videos()
    {
        return $this->morphedByMany(Video::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-retrieving-the-relationship"></a>
<!-- #### Retrieving The Relationship -->
#### Retrieving The Relationship

<!-- Once your database table and models are defined, you may access the relationships via your models. For example, to access all of the tags for a post, you may use the `tags` dynamic relationship property: -->
데이터베이스 테이블과 모델을 모두 정의했다면, 이제 모델을 통해 관계에 접근할 수 있습니다. 예를 들어, 하나의 게시글에 연결된 모든 태그를 조회하려면 `tags` 동적 관계 프로퍼티를 사용할 수 있습니다.

```
use App\Models\Post;

$post = Post::find(1);

foreach ($post->tags as $tag) {
    //
}
```

<!-- You may retrieve the parent of a polymorphic relation from the polymorphic child model by accessing the name of the method that performs the call to `morphedByMany`. In this case, that is the `posts` or `videos` methods on the `Tag` model: -->
다형성(Polymorphic) 자식 모델에서 `morphedByMany`를 호출하는 메서드 이름에 접근하여, 다형성 관계의 부모 모델을 조회할 수도 있습니다. 이 예시에서는 `Tag` 모델의 `posts` 또는 `videos` 메서드가 해당됩니다.

```
use App\Models\Tag;

$tag = Tag::find(1);

foreach ($tag->posts as $post) {
    //
}

foreach ($tag->videos as $video) {
    //
}
```

<a name="custom-polymorphic-types"></a>
<!-- ### Custom Polymorphic Types -->
### Custom Polymorphic Types

<!-- By default, Laravel will use the fully qualified class name to store the "type" of the related model. For instance, given the one-to-many relationship example above where a `Comment` model may belong to a `Post` or a `Video` model, the default `commentable_type` would be either `App\Models\Post` or `App\Models\Video`, respectively. However, you may wish to decouple these values from your application's internal structure. -->
기본적으로 Laravel은 연관된 모델의 "타입"을 저장할 때 **완전히 수식된 클래스명(fully qualified class name)** 을 사용합니다. 예를 들어, 앞서 소개한 일대다(One To Many) 관계 예시에서 `Comment` 모델이 `Post` 또는 `Video` 모델에 속하는 경우, 기본 `commentable_type` 값에는 각각 `App\Models\Post` 또는 `App\Models\Video`가 저장됩니다. 하지만, 애플리케이션의 내부 구조와 이 값들을 분리하고 싶을 수 있습니다.

<!-- For example, instead of using the model names as the "type", we may use simple strings such as `post` and `video`. By doing so, the polymorphic "type" column values in our database will remain valid even if the models are renamed: -->
예를 들어, 모델의 이름 대신에 `post`나 `video` 같은 간단한 문자열을 "타입"으로 사용할 수도 있습니다. 이렇게 하면 데이터베이스의 다형성 "타입" 컬럼 값이 모델의 이름이 바뀌더라도 여전히 유효하게 유지됩니다.

```
use Illuminate\Database\Eloquent\Relations\Relation;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);
```

<!-- You may call the `enforceMorphMap` method in the `boot` method of your `App\Providers\AppServiceProvider` class or create a separate service provider if you wish. -->
`enforceMorphMap` 메서드는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 호출하거나, 필요에 따라 별도의 서비스 프로바이더를 만들어 호출할 수도 있습니다.

<!-- You may determine the morph alias of a given model at runtime using the model's `getMorphClass` method. Conversely, you may determine the fully-qualified class name associated with a morph alias using the `Relation::getMorphedModel` method: -->
실행 중에 모델에서 사용하는 morph 별칭(alias)을 확인하려면 모델의 `getMorphClass` 메서드를 사용할 수 있습니다. 반대로, morph 별칭에 연결된 완전히 수식된 클래스명을 알아내려면 `Relation::getMorphedModel` 메서드를 이용하면 됩니다.

```
use Illuminate\Database\Eloquent\Relations\Relation;

$alias = $post->getMorphClass();

$class = Relation::getMorphedModel($alias);
```

> [!WARNING]
> 기존 애플리케이션에 "morph map"을 추가할 때, 데이터베이스 내의 모든 `*_type` 컬럼 값이 기존의 완전히 수식된 클래스명을 포함하고 있다면 반드시 새로 지정한 "맵" 이름으로 변환해주어야 합니다.

<a name="dynamic-relationships"></a>
<!-- ### Dynamic Relationships -->
### Dynamic Relationships

<!-- You may use the `resolveRelationUsing` method to define relations between Eloquent models at runtime. While not typically recommended for normal application development, this may occasionally be useful when developing Laravel packages. -->
`resolveRelationUsing` 메서드를 사용하면 Eloquent 모델 간의 관계를 런타임에 정의할 수 있습니다. 일반적인 애플리케이션 개발에서는 자주 사용하지 않지만, Laravel 패키지 개발 시에는 가끔 유용하게 쓸 수 있습니다.

<!-- The `resolveRelationUsing` method accepts the desired relationship name as its first argument. The second argument passed to the method should be a closure that accepts the model instance and returns a valid Eloquent relationship definition. Typically, you should configure dynamic relationships within the boot method of a [service provider](/docs/9.x/providers): -->
`resolveRelationUsing`는 첫 번째 인자로 원하는 관계 이름을 받고, 두 번째 인자로는 해당 모델 인스턴스를 받아 유효한 Eloquent 관계 정의를 반환하는 클로저를 받습니다. 보통 이 동적 관계 설정은 [service provider](/docs/9.x/providers)의 boot 메서드 내에서 구성해야 합니다.

```
use App\Models\Order;
use App\Models\Customer;

Order::resolveRelationUsing('customer', function ($orderModel) {
    return $orderModel->belongsTo(Customer::class, 'customer_id');
});
```

> [!WARNING]
> 동적 관계를 정의할 때는 반드시 Eloquent 관계 메서드에 명시적으로 키 이름 인자를 제공해야 합니다.

<a name="querying-relations"></a>
<!-- ## Querying Relations -->
## Querying Relations

<!-- Since all Eloquent relationships are defined via methods, you may call those methods to obtain an instance of the relationship without actually executing a query to load the related models. In addition, all types of Eloquent relationships also serve as [query builders](/docs/9.x/queries), allowing you to continue to chain constraints onto the relationship query before finally executing the SQL query against your database. -->
Eloquent의 모든 관계는 메서드를 통해 정의되어 있으므로, 해당 메서드를 호출하면 연관된 모델을 실제로 조회하지 않고도 관계의 인스턴스를 얻을 수 있습니다. 또한 모든 종류의 Eloquent 관계는 [query builders](/docs/9.x/queries)로 동작하므로, 최종적으로 DB에 쿼리를 실행하기 전에 관계 쿼리에 조건을 계속 체이닝할 수 있습니다.

<!-- For example, imagine a blog application in which a `User` model has many associated `Post` models: -->
예를 들어, 블로그 애플리케이션에서 `User` 모델이 여러 개의 `Post` 모델과 관계가 있다고 가정해봅시다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get all of the posts for the user.
     */
    public function posts()
    {
        return $this->hasMany(Post::class);
    }
}
```

<!-- You may query the `posts` relationship and add additional constraints to the relationship like so: -->
`posts` 관계를 조회하면서 추가 조건을 더할 수도 있습니다.

```
use App\Models\User;

$user = User::find(1);

$user->posts()->where('active', 1)->get();
```

<!-- You are able to use any of the Laravel [query builder's](/docs/9.x/queries) methods on the relationship, so be sure to explore the query builder documentation to learn about all of the methods that are available to you. -->
관계에서 Laravel [query builder's](/docs/9.x/queries)의 모든 메서드를 자유롭게 사용할 수 있으니, 사용 가능한 모든 메서드는 쿼리 빌더 문서를 참고해 익혀두는 것이 좋습니다.

<a name="chaining-orwhere-clauses-after-relationships"></a>
<!-- #### Chaining `orWhere` Clauses After Relationships -->
#### Chaining `orWhere` Clauses After Relationships

<!-- As demonstrated in the example above, you are free to add additional constraints to relationships when querying them. However, use caution when chaining `orWhere` clauses onto a relationship, as the `orWhere` clauses will be logically grouped at the same level as the relationship constraint: -->
앞선 예시처럼, 관계 쿼리에서 추가 조건을 자유롭게 체이닝할 수 있습니다. 다만, 관계에서 `orWhere` 절을 사용할 때는 특별히 주의해야 합니다. `orWhere`는 관계 조건과 같은 레벨로 논리적으로 그룹화되기 때문입니다.

```
$user->posts()
        ->where('active', 1)
        ->orWhere('votes', '>=', 100)
        ->get();
```

<!-- The example above will generate the following SQL. As you can see, the `or` clause instructs the query to return _any_ user with greater than 100 votes. The query is no longer constrained to a specific user: -->
위의 예시는 다음과 같은 SQL을 생성하게 됩니다. 보시다시피, `or` 절 때문에 투표 수가 100 이상인 **어느 사용자든** 결과에 포함될 수 있습니다. 이제 쿼리가 특정 사용자로 제한되지 않습니다.

```sql
select *
from posts
where user_id = ? and active = 1 or votes >= 100
```

<!-- In most situations, you should use [logical groups](/docs/9.x/queries#logical-grouping) to group the conditional checks between parentheses: -->
대부분의 경우, [logical groups](/docs/9.x/queries#logical-grouping)을 사용해 조건을 괄호로 그룹화하는 것이 좋습니다.

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
위의 예시는 다음과 같은 SQL을 생성합니다. 논리 그룹핑이 올바르게 되어 특정 사용자로 쿼리가 제한됩니다.

```sql
select *
from posts
where user_id = ? and (active = 1 or votes >= 100)
```

<a name="relationship-methods-vs-dynamic-properties"></a>
<!-- ### Relationship Methods Vs. Dynamic Properties -->
### Relationship Methods Vs. Dynamic Properties

<!-- If you do not need to add additional constraints to an Eloquent relationship query, you may access the relationship as if it were a property. For example, continuing to use our `User` and `Post` example models, we may access all of a user's posts like so: -->
Eloquent 관계 쿼리에 추가 조건이 필요 없다면, 해당 관계를 속성처럼 접근할 수 있습니다. 예를 들어, 앞에서 사용한 `User`와 `Post` 모델 예시에서, 한 사용자의 모든 게시글을 아래와 같이 가져올 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

foreach ($user->posts as $post) {
    //
}
```

<!-- Dynamic relationship properties perform "lazy loading", meaning they will only load their relationship data when you actually access them. Because of this, developers often use [eager loading](#eager-loading) to pre-load relationships they know will be accessed after loading the model. Eager loading provides a significant reduction in SQL queries that must be executed to load a model's relations. -->
동적 관계 프로퍼티는 "지연 로딩(lazy loading)"으로 동작하므로, 실제로 해당 속성에 접근하기 전까지는 관계 데이터가 로딩되지 않습니다. 이런 이유로, 개발자들은 모델을 불러온 후 반드시 접근할 연관관계를 미리 조회(즉시 로딩, eager loading)하는 [eager loading](#eager-loading) 기법을 자주 사용합니다. 즉시 로딩을 이용하면, 모델의 연관 데이터를 불러오기 위해 실행해야 하는 SQL 쿼리 수가 크게 줄어듭니다.

<a name="querying-relationship-existence"></a>
<!-- ### Querying Relationship Existence -->
### Querying Relationship Existence

<!-- When retrieving model records, you may wish to limit your results based on the existence of a relationship. For example, imagine you want to retrieve all blog posts that have at least one comment. To do so, you may pass the name of the relationship to the `has` and `orHas` methods: -->
모델 레코드를 조회할 때, 특정 관계가 존재하는지 여부로 결과를 제한하고 싶을 수 있습니다. 예를 들어, 댓글이 최소 하나 이상 달린 블로그 게시글만을 조회하고 싶다면, `has`와 `orHas` 메서드에 관계 이름을 인자로 전달하면 됩니다.

```
use App\Models\Post;

// Retrieve all posts that have at least one comment...
$posts = Post::has('comments')->get();
```

<!-- You may also specify an operator and count value to further customize the query: -->
추가로, 연산자와 개수 값을 지정해 쿼리를 조정할 수도 있습니다.

```
// Retrieve all posts that have three or more comments...
$posts = Post::has('comments', '>=', 3)->get();
```

<!-- Nested `has` statements may be constructed using "dot" notation. For example, you may retrieve all posts that have at least one comment that has at least one image: -->
중첩된 `has` 조건문은 "닷(dot) 표기법"을 사용해 만들 수 있습니다. 예를 들어, 최소 한 개 이상의 이미지가 달린 댓글이 있는 게시글을 모두 조회할 수 있습니다.

```
// Retrieve posts that have at least one comment with images...
$posts = Post::has('comments.images')->get();
```

<!-- If you need even more power, you may use the `whereHas` and `orWhereHas` methods to define additional query constraints on your `has` queries, such as inspecting the content of a comment: -->
더 복잡한 쿼리가 필요하다면, `has` 쿼리에 대해 `whereHas`와 `orWhereHas` 메서드를 사용해 추가 제약 조건(예: 댓글 내용 검사 등)을 지정할 수 있습니다.

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
> Eloquent는 현재 데이터베이스를 넘나드는 관계 존재 쿼리를 지원하지 않습니다. 관계는 반드시 동일한 데이터베이스 내에 존재해야 합니다.

<a name="inline-relationship-existence-queries"></a>
<!-- #### Inline Relationship Existence Queries -->
#### Inline Relationship Existence Queries

<!-- If you would like to query for a relationship's existence with a single, simple where condition attached to the relationship query, you may find it more convenient to use the `whereRelation`, `orWhereRelation`, `whereMorphRelation`, and `orWhereMorphRelation` methods. For example, we may query for all posts that have unapproved comments: -->
관계 쿼리에 매우 간단한 where 조건을 하나만 추가하고 싶을 때는 `whereRelation`, `orWhereRelation`, `whereMorphRelation`, `orWhereMorphRelation` 메서드가 더 편리할 수 있습니다. 예를 들어, 승인되지 않은(unapproved) 댓글이 달린 모든 게시글을 조회할 수 있습니다.

```
use App\Models\Post;

$posts = Post::whereRelation('comments', 'is_approved', false)->get();
```

<!-- Of course, like calls to the query builder's `where` method, you may also specify an operator: -->
물론, 쿼리 빌더의 `where` 메서드처럼 연산자를 지정할 수도 있습니다.

```
$posts = Post::whereRelation(
    'comments', 'created_at', '>=', now()->subHour()
)->get();
```

<a name="querying-relationship-absence"></a>
<!-- ### Querying Relationship Absence -->
### Querying Relationship Absence

<!-- When retrieving model records, you may wish to limit your results based on the absence of a relationship. For example, imagine you want to retrieve all blog posts that **don't** have any comments. To do so, you may pass the name of the relationship to the `doesntHave` and `orDoesntHave` methods: -->
모델 레코드를 조회할 때, 특정 관계가 **존재하지 않는** 경우만 결과에 포함하고 싶을 수 있습니다. 예를 들어, **댓글이 하나도 없는** 블로그 게시글만 조회하려면, `doesntHave`와 `orDoesntHave` 메서드에 관계 이름을 전달하면 됩니다.

```
use App\Models\Post;

$posts = Post::doesntHave('comments')->get();
```

<!-- If you need even more power, you may use the `whereDoesntHave` and `orWhereDoesntHave` methods to add additional query constraints to your `doesntHave` queries, such as inspecting the content of a comment: -->
더 복잡한 쿼리가 필요하다면, `doesntHave` 쿼리에 대해 `whereDoesntHave`와 `orWhereDoesntHave` 메서드를 사용해 추가 제약 조건(예: 댓글 내용 검사 등)을 지정할 수 있습니다.

```
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();
```

<!-- You may use "dot" notation to execute a query against a nested relationship. For example, the following query will retrieve all posts that do not have comments; however, posts that have comments from authors that are not banned will be included in the results: -->
"닷(dot)" 표기법을 사용해 중첩 관계에도 쿼리를 적용할 수 있습니다. 아래 쿼리는 댓글이 없는 게시글을 가져오는 대신, 금지(banned)되지 않은 저자가 쓴 댓글이 있는 게시글은 결과에 포함합니다.

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
"morph to" 관계의 존재를 쿼리할 때는 `whereHasMorph`와 `whereDoesntHaveMorph` 메서드를 사용할 수 있습니다. 이 메서드들은 첫 번째 인자로 관계 이름, 이어서 쿼리에 포함하고자 하는 연관 모델 이름 목록을 받습니다. 마지막으로, 관계 쿼리를 커스터마이즈할 수 있는 클로저를 전달할 수도 있습니다.

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
경우에 따라, 연관 다형성 모델의 "타입"에 기반해 쿼리 조건을 추가해야 할 수 있습니다. `whereHasMorph` 메서드에 전달하는 클로저는 두 번째 인자로 `$type` 값을 받을 수 있습니다. 이를 이용해 쿼리가 어떤 타입에 대해 만들어지고 있는지 검사할 수 있습니다.

```
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query, $type) {
        $column = $type === Post::class ? 'content' : 'title';

        $query->where($column, 'like', 'code%');
    }
)->get();
```

<a name="querying-all-morph-to-related-models"></a>
<!-- #### Querying All Related Models -->
#### Querying All Related Models

<!-- Instead of passing an array of possible polymorphic models, you may provide `*` as a wildcard value. This will instruct Laravel to retrieve all of the possible polymorphic types from the database. Laravel will execute an additional query in order to perform this operation: -->
다형성 관계에 연결 가능한 모델들을 배열로 전달하는 대신, `*`를 와일드카드 값으로 전달할 수도 있습니다. 그러면 Laravel은 데이터베이스에서 가능한 모든 다형성 타입을 조회해 자동으로 적용합니다. 이를 위해 Laravel이 한 번 더 쿼리를 실행합니다.

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
어떤 관계에 연결된 모델의 실제 데이터를 불러오지 않고도, 해당 개수가 몇 개인지 알고 싶을 때가 있습니다. 이럴 때는 `withCount` 메서드를 사용할 수 있습니다. `withCount`를 사용하면 결과 모델에 `{relation}_count` 속성이 추가됩니다.

```
use App\Models\Post;

$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->comments_count;
}
```

<!-- By passing an array to the `withCount` method, you may add the "counts" for multiple relations as well as add additional constraints to the queries: -->
`withCount`에 배열을 전달하면 여러 관계의 개수와 함께 쿼리에 추가 조건도 넣을 수 있습니다.

```
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount(['votes', 'comments' => function (Builder $query) {
    $query->where('content', 'like', 'code%');
}])->get();

echo $posts[0]->votes_count;
echo $posts[0]->comments_count;
```

<!-- You may also alias the relationship count result, allowing multiple counts on the same relationship: -->
관계 개수 결과에 별칭(alias)을 지정할 수도 있어서, 같은 관계에 대해 여러 번 개수를 셀 수도 있습니다.

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
`loadCount` 메서드를 이용해, 이미 조회한 부모 모델에서 나중에 관계 개수를 불러올 수 있습니다.

```
$book = Book::first();

$book->loadCount('genres');
```

<!-- If you need to set additional query constraints on the count query, you may pass an array keyed by the relationships you wish to count. The array values should be closures which receive the query builder instance: -->
개수 쿼리에 추가 제약 조건을 넣고 싶다면, 카운트할 관계명을 키로 하는 배열을 전달하면 됩니다. 배열 값은 쿼리 빌더 인스턴스를 받는 클로저여야 합니다.

```
$book->loadCount(['reviews' => function ($query) {
    $query->where('rating', 5);
}])
```

<a name="relationship-counting-and-custom-select-statements"></a>
<!-- #### Relationship Counting & Custom Select Statements -->
#### Relationship Counting & Custom Select Statements

<!-- If you're combining `withCount` with a `select` statement, ensure that you call `withCount` after the `select` method: -->
`withCount`와 `select`를 함께 쓸 경우, 반드시 `select` 호출 뒤에 `withCount`를 호출해야 합니다.

```
$posts = Post::select(['title', 'body'])
                ->withCount('comments')
                ->get();
```

<a name="other-aggregate-functions"></a>
<!-- ### Other Aggregate Functions -->
### Other Aggregate Functions

<!-- In addition to the `withCount` method, Eloquent provides `withMin`, `withMax`, `withAvg`, `withSum`, and `withExists` methods. These methods will place a `{relation}_{function}_{column}` attribute on your resulting models: -->
`withCount` 외에도 Eloquent에는 `withMin`, `withMax`, `withAvg`, `withSum`, `withExists` 메서드가 준비되어 있습니다. 이 메서드들은 결과 모델에 `{relation}_{function}_{column}` 속성을 추가합니다.

```
use App\Models\Post;

$posts = Post::withSum('comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->comments_sum_votes;
}
```

<!-- If you wish to access the result of the aggregate function using another name, you may specify your own alias: -->
집계 함수 결과를 다른 이름으로 접근하고 싶다면, 별칭(alias)을 지정할 수도 있습니다.

```
$posts = Post::withSum('comments as total_comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->total_comments;
}
```

<!-- Like the `loadCount` method, deferred versions of these methods are also available. These additional aggregate operations may be performed on Eloquent models that have already been retrieved: -->
`loadCount`와 마찬가지로, 이 집계 메서드들도 지연 버전이 제공됩니다. 이미 조회한 모델에 추가로 집계 연산을 적용할 수 있습니다.

```
$post = Post::first();

$post->loadSum('comments', 'votes');
```

<!-- If you're combining these aggregate methods with a `select` statement, ensure that you call the aggregate methods after the `select` method: -->
이 집계 메서드들을 `select`와 함께 사용할 때는 반드시 `select` 호출 뒤에 집계 메서드를 호출해야 합니다.

```
$posts = Post::select(['title', 'body'])
                ->withExists('comments')
                ->get();
```

<a name="counting-related-models-on-morph-to-relationships"></a>
<!-- ### Counting Related Models On Morph To Relationships -->
### Counting Related Models On Morph To Relationships

<!-- If you would like to eager load a "morph to" relationship, as well as related model counts for the various entities that may be returned by that relationship, you may utilize the `with` method in combination with the `morphTo` relationship's `morphWithCount` method. -->
"morph to" 관계를 즉시 로딩함과 동시에, 해당 관계가 반환할 수 있는 여러 엔티티별 연관 모델 개수를 함께 불러오고 싶을 때가 있습니다. 이때는 `with` 메서드와 `morphTo` 관계의 `morphWithCount` 메서드를 조합해 사용할 수 있습니다.

<!-- In this example, let's assume that `Photo` and `Post` models may create `ActivityFeed` models. We will assume the `ActivityFeed` model defines a "morph to" relationship named `parentable` that allows us to retrieve the parent `Photo` or `Post` model for a given `ActivityFeed` instance. Additionally, let's assume that `Photo` models "have many" `Tag` models and `Post` models "have many" `Comment` models. -->
여기서는 `Photo`와 `Post` 모델이 `ActivityFeed` 모델을 생성할 수 있다고 가정합니다. `ActivityFeed` 모델에는 주어진 `ActivityFeed` 인스턴스에 대한 부모 `Photo` 또는 `Post` 모델을 가져올 수 있도록 `parentable`이라는 "morph to" 관계가 정의되어 있다고 합시다. 또한, `Photo` 모델은 "여러" `Tag` 모델을, `Post` 모델은 "여러" `Comment` 모델을 가집니다.

<!-- Now, let's imagine we want to retrieve `ActivityFeed` instances and eager load the `parentable` parent models for each `ActivityFeed` instance. In addition, we want to retrieve the number of tags that are associated with each parent photo and the number of comments that are associated with each parent post: -->
이제, `ActivityFeed` 인스턴스들을 가져오면서 각 `ActivityFeed` 인스턴스에 연결된 부모 모델(`parentable`)을 즉시 로딩하고, 각 부모 사진의 태그 수와 각 부모 게시글의 댓글 수까지 함께 불러오고 싶다고 해봅시다.

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
이미 `ActivityFeed` 모델 세트를 조회한 이후에, 관련된 `parentable` 모델들의 관계 개수를 불러오고 싶다면, `loadMorphCount` 메서드를 사용할 수 있습니다.

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
Eloquent 관계에 속성으로 접근할 때, 연관된 모델은 "지연 로딩(lazy loading)"됩니다. 즉, 해당 속성에 처음 접근할 때까지는 관계 데이터가 실제로 로드되지 않습니다. 하지만, Eloquent에서는 부모 모델을 쿼리할 때 관계를 "즉시 로딩"할 수 있습니다. 즉시 로딩을 사용하면 "N + 1" 쿼리 문제를 완화할 수 있습니다. N + 1 문제의 예로, 한 `Book` 모델이 하나의 `Author` 모델(저자)에 속한다고 가정해 보겠습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Book extends Model
{
    /**
     * Get the author that wrote the book.
     */
    public function author()
    {
        return $this->belongsTo(Author::class);
    }
}
```

<!-- Now, let's retrieve all books and their authors: -->
이제 모든 책과 그 저자를 조회해 보겠습니다.

```
use App\Models\Book;

$books = Book::all();

foreach ($books as $book) {
    echo $book->author->name;
}
```

<!-- This loop will execute one query to retrieve all of the books within the database table, then another query for each book in order to retrieve the book's author. So, if we have 25 books, the code above would run 26 queries: one for the original book, and 25 additional queries to retrieve the author of each book. -->
위 반복문은 데이터베이스 테이블에서 모든 책을 가져오는 쿼리 하나를 실행하고, 각 책마다 해당 책의 저자를 조회하기 위해 또 다른 쿼리를 실행합니다. 즉, 책이 25권이라면, 총 26번(원본 쿼리 1번 + 저자 쿼리 25번) 쿼리가 실행됩니다.

<!-- Thankfully, we can use eager loading to reduce this operation to just two queries. When building a query, you may specify which relationships should be eager loaded using the `with` method: -->
다행히, 즉시 로딩을 사용하면 이 과정이 단 2개의 쿼리로 줄어듭니다. 쿼리를 작성할 때 `with` 메서드를 통해 즉시 로딩할 관계를 지정할 수 있습니다.

```
$books = Book::with('author')->get();

foreach ($books as $book) {
    echo $book->author->name;
}
```

<!-- For this operation, only two queries will be executed - one query to retrieve all of the books and one query to retrieve all of the authors for all of the books: -->
이렇게 하면 책 전체를 가져오는 쿼리 1번, 모든 책 저자를 한 번에 가져오는 쿼리 1번만 실행됩니다.

```sql
select * from books

select * from authors where id in (1, 2, 3, 4, 5, ...)
```

<a name="eager-loading-multiple-relationships"></a>

<!-- #### Eager Loading Multiple Relationships -->
#### Eager Loading Multiple Relationships

<!-- Sometimes you may need to eager load several different relationships. To do so, just pass an array of relationships to the `with` method: -->
여러 종류의 관계를 한 번에 eager 로딩해야 할 때가 있습니다. 이 경우, `with` 메서드에 관계들을 배열로 전달하면 됩니다.

```
$books = Book::with(['author', 'publisher'])->get();
```

<a name="nested-eager-loading"></a>
<!-- #### Nested Eager Loading -->
#### Nested Eager Loading

<!-- To eager load a relationship's relationships, you may use "dot" syntax. For example, let's eager load all of the book's authors and all of the author's personal contacts: -->
관계의 하위 관계까지 eager 로딩하려면 "점(dot) 표기법"을 사용할 수 있습니다. 예를 들어, 모든 책의 저자와 저자의 개인 연락처까지 eager 로딩하고 싶을 때 다음과 같이 작성할 수 있습니다.

```
$books = Book::with('author.contacts')->get();
```

<!-- Alternatively, you may specify nested eager loaded relationships by providing a nested array to the `with` method, which can be convenient when eager loading multiple nested relationships: -->
또는, 여러 중첩 관계를 한 번에 eager 로딩해야 할 경우, `with` 메서드에 중첩 배열 형태로 관계를 지정할 수 있습니다.

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
`morphTo` 관계와 해당 관계가 반환할 수 있는 다양한 엔티티에 대한 하위 관계까지 eager 로딩하고 싶을 경우, `with` 메서드와 `morphTo` 관계의 `morphWith` 메서드를 함께 사용할 수 있습니다. 설명을 돕기 위해 아래 모델을 예로 들어보겠습니다.

```
<?php

use Illuminate\Database\Eloquent\Model;

class ActivityFeed extends Model
{
    /**
     * Get the parent of the activity feed record.
     */
    public function parentable()
    {
        return $this->morphTo();
    }
}
```

<!-- In this example, let's assume `Event`, `Photo`, and `Post` models may create `ActivityFeed` models. Additionally, let's assume that `Event` models belong to a `Calendar` model, `Photo` models are associated with `Tag` models, and `Post` models belong to an `Author` model. -->
여기서 `Event`, `Photo`, `Post` 모델이 각각 `ActivityFeed` 모델을 생성할 수 있다고 가정합니다. 추가로, `Event` 모델은 `Calendar` 모델과 관계가 있고, `Photo` 모델은 `Tag` 모델에 연결되어 있으며, `Post` 모델은 `Author` 모델과 관계가 있다고 하겠습니다.

<!-- Using these model definitions and relationships, we may retrieve `ActivityFeed` model instances and eager load all `parentable` models and their respective nested relationships: -->
이 관계들을 바탕으로, 모든 `ActivityFeed` 인스턴스를 조회하고, 각각의 `parentable` 모델 및 이에 해당하는 하위 관계까지 eager 로딩하려면 다음과 같이 코드를 작성합니다.

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
모든 관계 모델의 모든 컬럼을 항상 사용할 필요는 없습니다. 이럴 때는, Eloquent에서 관계 모델의 필요한 컬럼만 지정해서 가져올 수 있습니다.

```
$books = Book::with('author:id,name,book_id')->get();
```

> [!WARNING]
> 이 기능을 사용할 때는 반드시 `id` 컬럼과, 해당 관계에 필요한 외래 키 컬럼을 컬럼 목록에 포함해야 합니다.

<a name="eager-loading-by-default"></a>
<!-- #### Eager Loading By Default -->
#### Eager Loading By Default

<!-- Sometimes you might want to always load some relationships when retrieving a model. To accomplish this, you may define a `$with` property on the model: -->
특정 관계를 모델을 조회할 때마다 항상 함께 불러오길 원할 때가 있습니다. 이럴 경우, 모델에 `$with` 속성을 정의하면 됩니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

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
    public function author()
    {
        return $this->belongsTo(Author::class);
    }

    /**
     * Get the genre of the book.
     */
    public function genre()
    {
        return $this->belongsTo(Genre::class);
    }
}
```

<!-- If you would like to remove an item from the `$with` property for a single query, you may use the `without` method: -->
특정 쿼리에서만 `$with`에 정의된 항목을 제외하고 싶을 때는 `without` 메서드를 사용할 수 있습니다.

```
$books = Book::without('author')->get();
```

<!-- If you would like to override all items within the `$with` property for a single query, you may use the `withOnly` method: -->
한 번의 쿼리에서 `$with` 속성에 있는 모든 관계를 재정의하려면, `withOnly` 메서드를 사용합니다.

```
$books = Book::withOnly('genre')->get();
```

<a name="constraining-eager-loads"></a>
<!-- ### Constraining Eager Loads -->
### Constraining Eager Loads

<!-- Sometimes you may wish to eager load a relationship but also specify additional query conditions for the eager loading query. You can accomplish this by passing an array of relationships to the `with` method where the array key is a relationship name and the array value is a closure that adds additional constraints to the eager loading query: -->
관계를 eager 로딩하면서 해당 쿼리에 추가 조건을 지정하고 싶을 때가 있습니다. 이 경우, `with` 메서드에 관계명-클로저 쌍으로 이루어진 배열을 전달하면 원하는 쿼리 제약 조건을 추가할 수 있습니다.

```
use App\Models\User;

$users = User::with(['posts' => function ($query) {
    $query->where('title', 'like', '%code%');
}])->get();
```

<!-- In this example, Eloquent will only eager load posts where the post's `title` column contains the word `code`. You may call other [query builder](/docs/9.x/queries) methods to further customize the eager loading operation: -->
위 예시에서는, 게시물의 `title` 컬럼에 `code`라는 단어가 포함된 게시글만 eager 로딩합니다. 다른 [query builder](/docs/9.x/queries) 메서드도 함께 사용할 수 있습니다.

```
$users = User::with(['posts' => function ($query) {
    $query->orderBy('created_at', 'desc');
}])->get();
```

> [!WARNING]
> `limit` 및 `take` 쿼리 빌더 메서드는 eager 로딩 쿼리를 제약할 때 사용할 수 없습니다.

<a name="constraining-eager-loading-of-morph-to-relationships"></a>
<!-- #### Constraining Eager Loading Of `morphTo` Relationships -->
#### Constraining Eager Loading Of `morphTo` Relationships

<!-- If you are eager loading a `morphTo` relationship, Eloquent will run multiple queries to fetch each type of related model. You may add additional constraints to each of these queries using the `MorphTo` relation's `constrain` method: -->
`morphTo` 관계를 eager 로딩하면, Eloquent는 각 관련 모델 타입마다 별도의 쿼리를 실행합니다. 이러한 각각의 쿼리에 별도의 제약조건을 추가하고 싶다면, `MorphTo` 관계의 `constrain` 메서드를 사용할 수 있습니다.

```
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Relations\MorphTo;

$comments = Comment::with(['commentable' => function (MorphTo $morphTo) {
    $morphTo->constrain([
        Post::class => function (Builder $query) {
            $query->whereNull('hidden_at');
        },
        Video::class => function (Builder $query) {
            $query->where('type', 'educational');
        },
    ]);
}])->get();
```

<!-- In this example, Eloquent will only eager load posts that have not been hidden and videos that have a `type` value of "educational". -->
이 예시에서는, 숨김 처리되지 않은 게시글과, `type`이 'educational'인 비디오만 eager 로딩됩니다.

<a name="constraining-eager-loads-with-relationship-existence"></a>
<!-- #### Constraining Eager Loads With Relationship Existence -->
#### Constraining Eager Loads With Relationship Existence

<!-- You may sometimes find yourself needing to check for the existence of a relationship while simultaneously loading the relationship based on the same conditions. For example, you may wish to only retrieve `User` models that have child `Post` models matching a given query condition while also eager loading the matching posts. You may accomplish this using the `withWhereHas` method: -->
관계가 존재하는지 확인하면서 동시에 해당 관계를 같은 조건으로 eager 로딩해야 할 때도 있습니다. 예를 들어, 자식 `Post` 모델이 특정 조건을 만족하는 경우에만 해당 `User` 모델을 조회하고, 그 게시글도 eager 로딩하고 싶을 때 `withWhereHas` 메서드를 사용할 수 있습니다.

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
경우에 따라, 부모 모델을 이미 조회한 뒤에 관계를 나중에 eager 로딩해야 할 수도 있습니다. 예를 들어, 동적으로 관련 모델을 불러올지 결정해야 하는 경우에 유용합니다.

```
use App\Models\Book;

$books = Book::all();

if ($someCondition) {
    $books->load('author', 'publisher');
}
```

<!-- If you need to set additional query constraints on the eager loading query, you may pass an array keyed by the relationships you wish to load. The array values should be closure instances which receive the query instance: -->
이 때 조건을 추가하고 싶다면, 로딩할 관계들을 키로 하고, 각 관계에 클로저를 값으로 갖는 배열을 전달할 수 있습니다.

```
$author->load(['books' => function ($query) {
    $query->orderBy('published_date', 'asc');
}]);
```

<!-- To load a relationship only when it has not already been loaded, use the `loadMissing` method: -->
이미 로딩된 적이 없는 관계만 불러오고 싶을 경우 `loadMissing` 메서드를 사용합니다.

```
$book->loadMissing('author');
```

<a name="nested-lazy-eager-loading-morphto"></a>
<!-- #### Nested Lazy Eager Loading & `morphTo` -->
#### Nested Lazy Eager Loading & `morphTo`

<!-- If you would like to eager load a `morphTo` relationship, as well as nested relationships on the various entities that may be returned by that relationship, you may use the `loadMorph` method. -->
`morphTo` 관계와, 그 관계가 반환하는 다양한 엔티티에 대한 하위 관계까지 한 번에 lazy eager 로딩하려면 `loadMorph` 메서드를 사용할 수 있습니다.

<!-- This method accepts the name of the `morphTo` relationship as its first argument, and an array of model / relationship pairs as its second argument. To help illustrate this method, let's consider the following model: -->
이 메서드는 첫 번째 인자로 `morphTo` 관계명을, 두 번째 인자로 모델 / 관계 쌍의 배열을 받습니다. 이해를 돕기 위해 다음 모델을 살펴보겠습니다.

```
<?php

use Illuminate\Database\Eloquent\Model;

class ActivityFeed extends Model
{
    /**
     * Get the parent of the activity feed record.
     */
    public function parentable()
    {
        return $this->morphTo();
    }
}
```

<!-- In this example, let's assume `Event`, `Photo`, and `Post` models may create `ActivityFeed` models. Additionally, let's assume that `Event` models belong to a `Calendar` model, `Photo` models are associated with `Tag` models, and `Post` models belong to an `Author` model. -->
여기서 `Event`, `Photo`, `Post` 모델이 각각 `ActivityFeed` 모델을 생성할 수 있다고 가정합니다. 추가로, `Event` 모델은 `Calendar` 모델과 관계가 있고, `Photo` 모델은 `Tag` 모델에 연결되어 있으며, `Post` 모델은 `Author` 모델과 관계가 있다고 하겠습니다.

<!-- Using these model definitions and relationships, we may retrieve `ActivityFeed` model instances and eager load all `parentable` models and their respective nested relationships: -->
앞서 설명한 모델 관계를 바탕으로, 모든 `ActivityFeed` 인스턴스를 불러오고 각각의 `parentable` 모델 및 하위 관계까지 eager 로딩하려면 다음과 같이 작성합니다.

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
앞서 살펴본 것처럼, 관계를 eager 로딩하면 애플리케이션의 성능이 크게 향상될 수 있습니다. 따라서 필요하다면, Laravel이 관계의 lazy 로딩을 항상 방지하도록 설정할 수도 있습니다. 이를 위해 Eloquent의 기본 모델 클래스가 제공하는 `preventLazyLoading` 메서드를 사용할 수 있습니다. 보통은 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출하면 됩니다.

<!-- The `preventLazyLoading` method accepts an optional boolean argument that indicates if lazy loading should be prevented. For example, you may wish to only disable lazy loading in non-production environments so that your production environment will continue to function normally even if a lazy loaded relationship is accidentally present in production code: -->
`preventLazyLoading` 메서드는 첫 번째 인자로 lazy 로딩을 방지할지 여부를 결정하는 불리언 값을 받습니다. 예를 들어, 운영(프로덕션) 환경이 아닐 때에만 lazy 로딩을 차단하도록 설정할 수 있습니다. 이렇게 하면 운영 환경에서 실수로 lazy 로딩 코드가 남아있더라도 장애가 발생하지 않습니다.

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

<!-- After preventing lazy loading, Eloquent will throw a `Illuminate\Database\LazyLoadingViolationException` exception when your application attempts to lazy load any Eloquent relationship. -->
이후 lazy 로딩을 방지하면, Eloquent가 관계를 lazy 로딩하려 하면 `Illuminate\Database\LazyLoadingViolationException` 예외를 발생시킵니다.

<!-- You may customize the behavior of lazy loading violations using the `handleLazyLoadingViolationsUsing` method. For example, using this method, you may instruct lazy loading violations to only be logged instead of interrupting the application's execution with exceptions: -->
또한, lazy 로딩 위반 발생 시의 동작을 `handleLazyLoadingViolationsUsing` 메서드로 커스터마이즈할 수 있습니다. 예를 들어, 이 메서드를 통해 애플리케이션 동작을 멈추는 대신, violation을 로그로만 남기도록 할 수도 있습니다.

```php
Model::handleLazyLoadingViolationUsing(function ($model, $relation) {
    $class = get_class($model);

    info("Attempted to lazy load [{$relation}] on model [{$class}].");
});
```

<a name="inserting-and-updating-related-models"></a>
<!-- ## Inserting & Updating Related Models -->
## Inserting & Updating Related Models

<a name="the-save-method"></a>
<!-- ### The `save` Method -->
### The `save` Method

<!-- Eloquent provides convenient methods for adding new models to relationships. For example, perhaps you need to add a new comment to a post. Instead of manually setting the `post_id` attribute on the `Comment` model you may insert the comment using the relationship's `save` method: -->
Eloquent는 관계에 새 모델을 추가하는 편리한 메서드를 제공합니다. 예를 들어, 게시물에 새 댓글을 추가해야 할 때가 있다고 해봅시다. 이때 직접 `Comment` 모델의 `post_id` 속성을 지정할 필요 없이, 관계의 `save` 메서드를 사용할 수 있습니다.

```
use App\Models\Comment;
use App\Models\Post;

$comment = new Comment(['message' => 'A new comment.']);

$post = Post::find(1);

$post->comments()->save($comment);
```

<!-- Note that we did not access the `comments` relationship as a dynamic property. Instead, we called the `comments` method to obtain an instance of the relationship. The `save` method will automatically add the appropriate `post_id` value to the new `Comment` model. -->
위 코드에서, 동적 속성으로서 `comments` 관계에 접근한 것이 아니라, `comments` 메서드를 호출해 관계 인스턴스를 얻었습니다. `save` 메서드는 새 `Comment` 모델에 적절한 `post_id` 값을 자동으로 채워줍니다.

<!-- If you need to save multiple related models, you may use the `saveMany` method: -->
여러 연관된 모델을 한 번에 저장해야 한다면 `saveMany` 메서드를 사용할 수 있습니다.

```
$post = Post::find(1);

$post->comments()->saveMany([
    new Comment(['message' => 'A new comment.']),
    new Comment(['message' => 'Another new comment.']),
]);
```

<!-- The `save` and `saveMany` methods will persist the given model instances, but will not add the newly persisted models to any in-memory relationships that are already loaded onto the parent model. If you plan on accessing the relationship after using the `save` or `saveMany` methods, you may wish to use the `refresh` method to reload the model and its relationships: -->
`save`와 `saveMany` 메서드는 전달한 모델 인스턴스를 영구적으로 데이터베이스에 저장하지만, 이 과정에서 부모 모델에 이미 로드된 in-memory 관계에 새로 저장된 모델이 자동으로 추가되지는 않습니다. `save`나 `saveMany` 메서드를 사용한 뒤에 관계에 접근할 계획이 있다면, `refresh` 메서드로 모델과 그 관계를 다시 로드하는 것이 좋습니다.

```
$post->comments()->save($comment);

$post->refresh();

// All comments, including the newly saved comment...
$post->comments;
```

<a name="the-push-method"></a>
<!-- #### Recursively Saving Models & Relationships -->
#### Recursively Saving Models & Relationships

<!-- If you would like to `save` your model and all of its associated relationships, you may use the `push` method. In this example, the `Post` model will be saved as well as its comments and the comment's authors: -->
자신의 모델과, 연결된 관계까지 한 번에 모두 `save`하고 싶을 때는 `push` 메서드를 사용할 수 있습니다. 아래 예시에서는 `Post` 모델과, 그 댓글 및 각 댓글의 작성자까지 모두 저장됩니다.

```
$post = Post::find(1);

$post->comments[0]->message = 'Message';
$post->comments[0]->author->name = 'Author Name';

$post->push();
```

<!-- The `pushQuietly` method may be used to save a model and its associated relationships without raising any events: -->
이벤트를 발생시키지 않고 조용히 모델과 관계를 저장하고 싶다면 `pushQuietly` 메서드를 사용할 수 있습니다.

```
$post->pushQuietly();
```

<a name="the-create-method"></a>
<!-- ### The `create` Method -->
### The `create` Method

<!-- In addition to the `save` and `saveMany` methods, you may also use the `create` method, which accepts an array of attributes, creates a model, and inserts it into the database. The difference between `save` and `create` is that `save` accepts a full Eloquent model instance while `create` accepts a plain PHP `array`. The newly created model will be returned by the `create` method: -->
`save`, `saveMany` 메서드 외에, 속성 배열을 받아서 모델을 생성하고 데이터베이스에 바로 저장하는 `create` 메서드도 사용할 수 있습니다. `save`와 `create`의 차이는, `save`는 완전한 Eloquent 모델 인스턴스를 요구하는 반면 `create`는 단순 PHP `array`를 인수로 받는다는 점입니다. `create`는 새로 생성한 모델을 반환합니다.

```
use App\Models\Post;

$post = Post::find(1);

$comment = $post->comments()->create([
    'message' => 'A new comment.',
]);
```

<!-- You may use the `createMany` method to create multiple related models: -->
여러 연관된 모델을 한 번에 생성하려면 `createMany` 메서드를 사용할 수 있습니다.

```
$post = Post::find(1);

$post->comments()->createMany([
    ['message' => 'A new comment.'],
    ['message' => 'Another new comment.'],
]);
```

<!-- You may also use the `findOrNew`, `firstOrNew`, `firstOrCreate`, and `updateOrCreate` methods to [create and update models on relationships](/docs/9.x/eloquent#upserts). -->
또한, `findOrNew`, `firstOrNew`, `firstOrCreate`, `updateOrCreate` 등의 메서드를 이용하여 [create and update models on relationships](/docs/9.x/eloquent#upserts)할 수도 있습니다.

> [!NOTE]
> `create` 메서드를 사용하기 전에, 반드시 [mass assignment](/docs/9.x/eloquent#mass-assignment) 문서를 확인해야 합니다.

<a name="updating-belongs-to-relationships"></a>
<!-- ### Belongs To Relationships -->
### Belongs To Relationships

<!-- If you would like to assign a child model to a new parent model, you may use the `associate` method. In this example, the `User` model defines a `belongsTo` relationship to the `Account` model. This `associate` method will set the foreign key on the child model: -->
자식 모델을 새 부모 모델에 연결하려면 `associate` 메서드를 사용할 수 있습니다. 예를 들어, `User` 모델이 `Account` 모델과 `belongsTo` 관계를 정의한다고 가정하고, `associate` 메서드를 통해 자식 모델의 외래 키 값을 설정합니다.

```
use App\Models\Account;

$account = Account::find(10);

$user->account()->associate($account);

$user->save();
```

<!-- To remove a parent model from a child model, you may use the `dissociate` method. This method will set the relationship's foreign key to `null`: -->
자식 모델에서 부모 모델을 제거하려면 `dissociate` 메서드를 사용합니다. 이 메서드는 관계의 외래 키를 `null`로 설정합니다.

```
$user->account()->dissociate();

$user->save();
```

<a name="updating-many-to-many-relationships"></a>
<!-- ### Many To Many Relationships -->
### Many To Many Relationships

<a name="attaching-detaching"></a>
<!-- #### Attaching / Detaching -->
#### Attaching / Detaching

<!-- Eloquent also provides methods to make working with many-to-many relationships more convenient. For example, let's imagine a user can have many roles and a role can have many users. You may use the `attach` method to attach a role to a user by inserting a record in the relationship's intermediate table: -->
Eloquent는 다대다 관계를 좀 더 쉽게 다룰 수 있도록 여러 메서드를 제공합니다. 예를 들어, 한 사용자가 여러 역할(role)을 가질 수 있고, 하나의 역할도 여러 사용자를 가질 수 있다고 가정합니다. 사용자를 역할에 연결하려면, 관계의 중간 테이블에 레코드를 삽입하는 `attach` 메서드를 사용합니다.

```
use App\Models\User;

$user = User::find(1);

$user->roles()->attach($roleId);
```

<!-- When attaching a relationship to a model, you may also pass an array of additional data to be inserted into the intermediate table: -->
관계를 연결할 때, 중간 테이블에 추가로 저장해야 할 데이터가 있다면 배열로 전달할 수 있습니다.

```
$user->roles()->attach($roleId, ['expires' => $expires]);
```

<!-- Sometimes it may be necessary to remove a role from a user. To remove a many-to-many relationship record, use the `detach` method. The `detach` method will delete the appropriate record out of the intermediate table; however, both models will remain in the database: -->
때로는 사용자의 역할을 제거해야 할 필요도 있습니다. 이때는 `detach` 메서드를 사용하면 됩니다. `detach`는 관계의 중간 테이블에서 해당 레코드만 삭제하고, 두 모델은 그대로 남아있습니다.

```
// Detach a single role from the user...
$user->roles()->detach($roleId);

// Detach all roles from the user...
$user->roles()->detach();
```

<!-- For convenience, `attach` and `detach` also accept arrays of IDs as input: -->
`attach`와 `detach` 메서드는 편의상 ID 배열을 인자로 받아 여러 관계를 한 번에 처리할 수도 있습니다.

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
다대다 관계를 구성할 때 `sync` 메서드를 사용할 수도 있습니다. `sync` 메서드는 중간 테이블에 포함해야 할 ID 배열을 받으며, 배열에 없는 ID는 중간 테이블에서 삭제합니다. 즉, 이 작업이 끝나면 지정한 ID들만 중간 테이블에 남게 됩니다.

```
$user->roles()->sync([1, 2, 3]);
```

<!-- You may also pass additional intermediate table values with the IDs: -->
ID와 함께 중간 테이블에 값을 추가로 저장하고 싶다면 다음처럼 작성할 수 있습니다.

```
$user->roles()->sync([1 => ['expires' => true], 2, 3]);
```

<!-- If you would like to insert the same intermediate table values with each of the synced model IDs, you may use the `syncWithPivotValues` method: -->
여러 ID에 대해 같은 중간 테이블 값을 삽입하려면 `syncWithPivotValues` 메서드를 사용할 수 있습니다.

```
$user->roles()->syncWithPivotValues([1, 2, 3], ['active' => true]);
```

<!-- If you do not want to detach existing IDs that are missing from the given array, you may use the `syncWithoutDetaching` method: -->
이미 연결된 ID 중, 배열에 없는 걸 제거하고 싶지 않다면 `syncWithoutDetaching` 메서드를 사용할 수 있습니다.

```
$user->roles()->syncWithoutDetaching([1, 2, 3]);
```

<a name="toggling-associations"></a>
<!-- #### Toggling Associations -->
#### Toggling Associations

<!-- The many-to-many relationship also provides a `toggle` method which "toggles" the attachment status of the given related model IDs. If the given ID is currently attached, it will be detached. Likewise, if it is currently detached, it will be attached: -->
다대다 관계는 지정한 관련 모델 ID의 연결 상태를 "토글"하는 `toggle` 메서드도 제공합니다. 현재 연결되어 있으면 분리, 분리되어 있으면 연결합니다.

```
$user->roles()->toggle([1, 2, 3]);
```

<!-- You may also pass additional intermediate table values with the IDs: -->
ID와 함께 중간 테이블 값을 추가로 저장해야 할 땐 이렇게 사용할 수도 있습니다.

```
$user->roles()->toggle([
    1 => ['expires' => true],
    2 => ['expires' => true],
]);
```

<a name="updating-a-record-on-the-intermediate-table"></a>
<!-- #### Updating A Record On The Intermediate Table -->
#### Updating A Record On The Intermediate Table

<!-- If you need to update an existing row in your relationship's intermediate table, you may use the `updateExistingPivot` method. This method accepts the intermediate record foreign key and an array of attributes to update: -->
관계의 중간 테이블에 존재하는 특정 행을 업데이트해야 한다면, `updateExistingPivot` 메서드를 사용할 수 있습니다. 이 메서드는 중간 레코드의 외래 키와, 업데이트할 속성 배열을 받습니다.

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
모델이 `belongsTo` 또는 `belongsToMany` 관계를 가지고 있을 경우, 예를 들어, `Comment`가 `Post`에 속해 있다면, 자식 모델이 업데이트될 때 부모 모델의 타임스탬프도 같이 업데이트되고 싶을 때가 있습니다.

<!-- For example, when a `Comment` model is updated, you may want to automatically "touch" the `updated_at` timestamp of the owning `Post` so that it is set to the current date and time. To accomplish this, you may add a `touches` property to your child model containing the names of the relationships that should have their `updated_at` timestamps updated when the child model is updated: -->
예를 들어, `Comment` 모델이 업데이트될 때 소유한 `Post`의 `updated_at` 타임스탬프를 현재 시각으로 자동 갱신하고 싶을 경우, 자식 모델에 `touches` 속성을 추가하여, 해당 모델이 업데이트될 때 같이 `updated_at` 타임스탬프를 갱신할 관계명을 지정하면 됩니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

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
    public function post()
    {
        return $this->belongsTo(Post::class);
    }
}
```

> [!WARNING]
> 부모 모델의 타임스탬프는 자식 모델을 Eloquent의 `save` 메서드로 업데이트 할 때만 갱신됩니다.
