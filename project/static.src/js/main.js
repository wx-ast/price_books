$(function() {
    (function() {
        var task_links = $('.js_async_task');

        var check_status = function(task_ids, task_type) {
            main.query({
                url: '/async_task_status/',
                data: {
                    task_ids: task_ids.join(';'),
                    task_type: task_type
                },
                success: function(response) {
                    if (typeof response['status'] !== 'undefined') {
                        var task_ids = []
                        for (var task_id in response['status']) {
                            var status = response['status'][task_id]['status'];
                            var link = task_links.filter('[data-task_id="' + task_id + '"]');
                            if (status == 'PENDING') {
                                task_ids.push(task_id);
                                link.addClass('js_async_task_pending');
                            } else if (status == 'SUCCESS') {
                                link.addClass('js_async_task_success');
                            } else if (status == 'FAILURE') {
                                link.addClass('js_async_task_failure');
                            }
                            link.text(response['status'][task_id]['text'])
                        }
                        if (task_ids.length > 0) {
                            setTimeout(check_status, 1000, task_ids, task_type);
                        }
                    }
                },
                error: function(error) {
                    $('.message').text('Ошибка');
                }
            });
        }
        if (task_links.length > 0) {
            var task_ids = [];
            var task_type = '';
            task_links.each(function() {
                task_ids.push($(this).data('task_id'));
                $(this).addClass('js_async_task_new');

                if (task_type.length <= 0 && $(this).data('task_type').length > 0) {
                    task_type = $(this).data('task_type');
                }
            });
            setTimeout(check_status, 1000, task_ids, task_type);
        }
    })();

    (function() {
        var csrftoken = Cookies.get('csrftoken');

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
    })();
});

var main = {
    query: function(options) {
        var defaultOptions = {
            url: '/ajax/',
            html: false,
            error: function(error) {
                console.log(error);
            },
            data: {}
        };

        return (function(options) {
            var opt = $.extend({}, defaultOptions, options);

            if (typeof opt.action !== 'undefined') {
                opt.data['tag'] = opt.action;
            }
            $.ajax({
                type: "POST",
                url: opt.url,
                data: opt.data,
                timeout: 10000,
                dataType : opt.html ? 'html' : 'json',
                success: function(data) {
                    if (typeof data !== 'undefined' && data !== null) {
                        if (typeof data.error !== 'undefined' && typeof opt.error !== 'undefined') {
                            opt.error(data.error);
                        } else {
                            if (typeof opt.success !== 'undefined') {
                                opt.success(data);
                            }
                        }

                        if (typeof data.log !== 'undefined') {
                            console.log('log: ' + data.log);
                        }
                    }
                },
                error: function(XMLHttpRequest, textStatus, errorThrow) {
                    if (textStatus == 'parsererror') {
                        console.log(XMLHttpRequest.responseText);
                    }
                    if (typeof opt.error !== 'undefined') {
                        opt.error(textStatus);
                    }
                    return true;
                }
            });
        })(options);
    },
};
