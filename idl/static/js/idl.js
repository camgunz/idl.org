function setFormSuccess(form_id, text) {
    var loading_image = $('#' + form_id + ' img.loading');
    if (text != null && text.length > 0) {
        loading_image.hide().after('<span class="success">' + text + '</span>');
    }
    else {
        loading_image.hide();
    }
}

function setFormError(form_id, text) {
    var loading_image = $('#' + form_id + ' img.loading');
    if (text != null && text.length > 0) {
        loading_image.hide().after('<span class="error">' + text + '</span>');
    }
    else {
        loading_image.hide();
    }
}

function clearForm(form_id) {
    $('.error').remove();
    $('.success').remove();
    $('#' + form_id + ' img.loading').show();
}

function wrapForm(form_id, submit_text, submit_func, loading_size) {
    var loading_url = static_url + '/images/loading-' + loading_size + '.gif';
    var img = '<img class="loading" src="' + loading_url + '"/>';
    var button = $('<button></button>').text(submit_text).click(submit_func);
    $('#' + form_id + ' > input').keypress(function (e) {
        var keychar;
        if (window.event) { // Old IE
            keychar = e.keyCode;
        }
        else if (e.which) { // Something else
            keychar = e.which;
        }
        if (keychar == 13) {
            submit_func();
        }
    });
    $('#' + form_id).append(img).append(button);
}

function sendLogin() {
    clearForm('login_form');
    var username_field_value = $('#username').val();
    var password_field_value = $('#password').val();
    if (username_field_value.length < 1 || password_field_value.length < 1) {
        setFormError('login_form', 'All fields required.');
        return;
    }
    $.ajax({
        type: 'POST',
        url: '/login',
        data: $.param({
            username: username_field_value,
            password: password_field_value
        }),
        success: function (data, text_status, xhr) {
            setFormSuccess('login_form');
            $('#account_box').html(data);
            $.ajax({
                url: '/profiles/players/' + username_field_value,
                success: function (d) { $('#player_profile').html(d) }
            });
        },
        error: function (xhr, status, error) {
            if (xhr.status == 401) {
                var error = 'Login failed';
            }
            else {
                error = 'Internal Server Error';
            }
            setFormError('login_form', error);
        }
    });
}

function sendPlayerSearch() {
    var player_name_field_value = $('#player_name').val();
    if (player_name_field_value.length < 1) {
        setFormError('login_form', "Please enter a player's name.");
        return;
    }
    $.ajax({
        type: 'GET',
        url: '/profiles/players',
        data: $.param({ player_name: player_name_field_value }),
        success: function (data, text_status, xhr) {
            $('#player_profile_search_results').html(data)
        },
        error: function (xhr, status, error) {
            if (xhr.status == 401) {
                var error = 'Login failed';
            }
            else {
                var error = xhr.responseText;
            }
            if (error == 'None') {
                error = 'Internal Server Error';
            }
            setFormError('login_form', error);
        }
    });
}

function sendSeasonSelection() {
    window.location.search = '?season=' + $('#season_id').val();
}

function hideAllCalendars() {
    $('div.calendar').hide();
}

function zeroPad(s) {
    if (s.length < 2) {
        s = '0' + s;
    }
    return s
}

function dateToString(d) {
    var year = d.getFullYear();
    var month = d.getMonth() + 1;
    var day = d.getDate();
    var hour = d.getHours();
    var minute = d.getMinutes();
    var second = d.getSeconds();
    var str_date = year + '-' + month  + '-' + day;
    var str_time = hour + ':' + minute + ':' + second;
    return str_date + ' ' + str_time;
}

function junkToTimestamp(year, month, hour, minute) {
    month = zeroPad(month.toString());
    hour = zeroPad(hour.toString());
    minute = zeroPad(minute.toString());
    return year + '-' + month  + '-01 ' + hour + ':' + minute + ':00';
}

function calendar(timestamp, mclass, eid, eclass, deid, hidden) {
    if (hidden == null) {
        hidden = false;
    }
    if (timestamp == null) {
        var d = new Date();
        year = d.getFullYear();
        month = d.getMonth() + 1;
        month = zeroPad(month.toString());
        day = '01';
        hour = d.getHour();
        hour = zeroPad(hour.toString());
        minute = d.getMinute();
        minute = zeroPad(minute.toString());
        second = '00';
        timestamp = year + '-' + month  + '-' + day    + ' ' + 
                    hour + ':' + minute + ':' + second;
    }
    $.ajax({
        type: 'GET',
        url: '/admin/calendar',
        data: $.param({
            timestamp: timestamp,
            mclass: mclass,
            eid: eid,
            eclass: eclass,
            deid: deid,
            hidden: hidden
        }),
        success: function (data, text_status, xhr) {
            $('#' + eid).html(data);
        },
        error: function (xhr, status, error) {
            $('#error').html(error);
        }
    });
}

function previousMonth(year, month, hour, minute, mclass, eid, eclass, deid,
                       hidden) {
    month--;
    if (month < 1) {
        month = 12;
        year--;
    }
    var timestamp = junkToTimestamp(year, month, hour, minute);
    calendar(timestamp, mclass, eid, eclass, deid, hidden);
}

function nextMonth(year, month, hour, minute, mclass, eid, eclass, deid,
                   hidden) {
    month++;
    if (month > 12) {
        month = 1;
        year++;
    }
    var timestamp = junkToTimestamp(year, month, hour, minute);
    calendar(timestamp, mclass, eid, eclass, deid, hidden);
}

function setDateTime(element_id, year, month, day) {
    var field = $('#' + element_id);
    var ts_array = field.val().split(' ');
    if (month < 10) {
        month = '0' + month;
    }
    if (day < 10) {
        day = '0' + day;
    }
    hour = $('#cal_hour').val();
    minute = $('#cal_minute').val();
    ts_array[0] = year + '-' + month + '-' + day;
    ts_array[1] = hour + ':' + minute + ':00';
    field.val(ts_array[0] + ' ' + ts_array[1]);
}

function setTime(element_id) {
    var field = $('#' + element_id);
    var ts_array = field.val().split(' ');
    if (ts_array[0] == undefined || ts_array[1] == undefined) {
        return;
    }
    hour = $('#cal_hour').val();
    minute = $('#cal_minute').val();
    ts_array[1] = hour + ':' + minute + ':00';
    field.val(ts_array[0] + ' ' + ts_array[1]);
}

function hideSuccessAndError() {
    $('#success').hide();
    $('#error').hide();
}

function setSuccess(msg) {
    $('#error').hide();
    $('#success').html(msg).show();
}

function setError(error) {
    $('#success').hide();
    $('#error').html(error).show();
}

function demoUploadStarted() {
    hideSuccessAndError();
    $('#uploading').css('display', 'inline');
    $('#submit_demo').css('display', 'none');
}

function demoUploadCompleted(error) {
    // [CG] I know about .hide(), but this is more orthogonal with
    //      demoUploadStarted() above.
    $('#uploading').css('display', 'none');
    $('#submit_demo').css('display', 'inline');

    if (error && error != 'null') {
        setError('Error: ' + error);
    }
    else {
        setSuccess('Demo uploaded successfully');
    }
    $('#demo_data').val('');
}

function adminLogUploadStarted() {
    hideSuccessAndError();
    $('#uploading').css('display', 'inline');
}

function adminLogUploadCompleted(error) {
    // [CG] I know about .hide(), but this is more orthogonal with
    //      adminLogUploadStarted() above.
    $('#uploading').css('display', 'none');

    if (error && error != 'null') {
        setError('Error: ' + error);
    }
    else {
        setSuccess('Log uploaded successfully');
    }
    $('#game_log_data').val('');
}

function adminShowLogUpload(junk) {
    hideSuccessAndError();
    var entry = $('#admin_select').val();
    if (entry == null || entry == '') {
        return;
    }
    $.ajax({
        type: 'GET',
        url: '/admin/game_logs',
        data: $.param({
            module: 'Game',
            entry: entry
        }),
        success: function (data, text_status, xhr) {
            loadAdminEntry(data);
        },
        error: function (xhr, status, error) {
            setError(error);
        }
    });
}

function adminList(module) {
    hideSuccessAndError();
    if (module == null) {
        return;
    }
    $.ajax({
        type: 'GET',
        url: '/admin/list',
        data: $.param({
            module: module
        }),
        success: function (data, text_status, xhr) {
            $('#admin_list').html(data);
        },
        error: function (xhr, status, error) {
            setError(error);
        }
    });
    $('#admin_entry').html('');
}

function toggleChecked(checkbox) {
    if(checkbox.checked) {
        $(checkbox).val("on");
    }
    else {
        $(checkbox).val("off");
    }
}

function loadAdminEntry(data) {
    $('#admin_entry').html(data);
    $('input:checkbox').each(function (index, x) {
        var element = $(x);
        if (element.val() == "on") {
            element.attr("checked", true);
        }
        else {
            element.attr("checked", false);
        }
    });
}

function adminGet(module) {
    hideSuccessAndError();
    if (module == null) {
        return;
    }
    var entry = $('#admin_select').val();
    if (entry == null || entry == '') {
        return;
    }
    $.ajax({
        type: 'GET',
        url: '/admin/get',
        data: $.param({
            module: module,
            entry: entry
        }),
        success: function (data, text_status, xhr) {
            loadAdminEntry(data);
        },
        error: function (xhr, status, error) {
            setError(error);
        }
    });
}

function adminSet(module, attributes) {
    hideSuccessAndError();
    if (module == null) {
        return;
    }
    data = {};
    $.each(attributes, function (i, v) {
        var el = $('#' + v);
        data[v] = el.val();
    });
    data.module = module;
    data.entry = $('#entry_id').val();
    if (!data.entry) {
        var url = '/admin/new';
    }
    else {
        var url = '/admin/set';
    }
    $.ajax({
        type: 'POST',
        url: url,
        data: $.param(data),
        success: function (data, text_status, xhr) {
            setSuccess('Successfully updated.');
            loadAdminEntry(data);
        },
        error: function (xhr, status, error) {
            setError(error);
        }
    });
}

function adminDelete(module, name) {
    hideSuccessAndError();
    if (module == null) {
        return;
    }
    var entry = $('admin_select').val();
    if (entry == null || entry == '') {
        return;
    }
    if (confirm("Are you sure you want to delete this entry?")) {
        $.ajax({
            type: 'POST',
            url: '/admin/delete',
            data: $.param({
                module: module,
                entry: entry
            }),
            success: function (data, text_status, xhr) {
                setSuccess('Successfully deleted.');
                $('#admin_entry').html('');
                $('#admin_delete').hide();
                adminList(name);
            },
            error: function (xhr, status, error) {
                setError(error);
            }
        });
    }
}

function adminNew(module) {
    hideSuccessAndError();
    if (module == null) {
        return;
    }
    // [CG] adminNew only requests a new, blank entry form.  adminSet submits
    //      the new data.  Therefore this uses GET and adminSet uses POST.
    $.ajax({
        type: 'GET',
        url: '/admin/new',
        data: $.param({
            module: module
        }),
        success: function (data, text_status, xhr) {
            $('#admin_entry').html(data);
        }
    });
}

$(document).ready(function() {
    wrapForm('player_search_form', 'Search', sendPlayerSearch, 'large');
    wrapForm('season_select_form', 'Go', sendSeasonSelection, 'large');
    wrapForm('login_form', 'Login', sendLogin, 'medium');
    hideSuccessAndError();
});

