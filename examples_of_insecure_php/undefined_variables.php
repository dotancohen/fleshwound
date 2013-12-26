<?php

$valid = "Something valid";
$this_var_is_in_context_in_the_function = 'silly';
$this_var_is_not_in_context_in_the_function = 'silly';


echo $valid;
echo $invalid;


if ( $valid=='yes' ) {
	echo 'yes';
}

if ( $invalid=='yes' ) {
	echo 'yes';
}

if ( $valid=='yes' || $invalid=='yes' ) {
	echo 'yes';
}

if ( $invalid=='yes' || $valid=='yes' ) {
	echo 'yes';
}



function someFunction($valid_variable)
{
	global $this_var_is_in_context_in_the_function;

	echo $invalid;
	echo $valid_variable;
	echo $this_var_is_in_context_in_the_function;
	echo $this_var_is_not_in_context_in_the_function;

	return TRUE;
}


?>
