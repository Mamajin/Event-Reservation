import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { LuTrash2 } from "react-icons/lu";
import { FiEdit2, FiMessageSquare } from "react-icons/fi";
import api from '../../../api';

export function CommentSection({ event }) {
  const [comments, setComments] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors }
  } = useForm();
}
