import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { LuTrash2, LuSend, LuCheck, LuX } from "react-icons/lu";
import { FiEdit2, FiMessageSquare } from "react-icons/fi";
import api from '../../../api';
import { USER_ID } from '../../../constants';
import { HiOutlineDotsVertical } from "react-icons/hi";
import { ACCESS_TOKEN } from '../../../constants';

export function CommentSection({ event }) {
  const [comments, setComments] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [editContent, setEditContent] = useState(''); 
  const [comment, setComment] = useState('');
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const userId = localStorage.getItem(USER_ID);
  const {
    handleSubmit,
    reset,
    formState: { errors }
  } = useForm();

  // API endpoints
  const end_point = {
    getEventComments: async (eventId) => {
      try {
        const token = localStorage.getItem(ACCESS_TOKEN);
        const headers = {
          Authorization: `Bearer ${token}`,
        };
        const response = await api.get(`/events/${eventId}/comments`, { headers });
        return response.data;
      } catch (error) {
        throw new Error('Error fetching comments: ' + (error.response?.data?.detail));
      }
    },
    writeComment: async (content, eventId) => {
      try {
        const token = localStorage.getItem(ACCESS_TOKEN);
        const headers = {
          Authorization: `Bearer ${token}`,
        };
        const response = await api.post(`/comments/write-comment/${eventId}`, { content }, { headers });
        return response.data;
      } catch (error) {
        throw new Error('Error creating comment: ' + (error.response?.data?.detail));
      }
    },
    deleteComment: async (commentId) => {
      try {
        const token = localStorage.getItem(ACCESS_TOKEN);
        const headers = {
          Authorization: `Bearer ${token}`,
        };
        const response = await api.delete(`/comments/${commentId}/delete/`, { headers });
        return response.status === 204;
      } catch (error) {
        throw new Error('Error deleting comment: ' + (error.response?.data?.detail));
      }
    },
    editComment: async (commentId, content) => {
      try {
        const token = localStorage.getItem(ACCESS_TOKEN);
        const headers = {
          Authorization: `Bearer ${token}`,
        };
        const response = await api.put(`/comments/${commentId}/edit/`, { content }, { headers });
        return response.data;
      } catch (error) {
        throw new Error('Error editing comment: ' + (error.response?.data?.detail));
      }
    }
  };

  // Fetch comments on component mount or when event changes
  useEffect(() => {
    const fetchComments = async () => {
      if (!event?.id) return;
      try {
        setIsLoading(true);
        const fetchedComments = await end_point.getEventComments(event.id);
        setComments(fetchedComments);
      } catch (error) {
        setError(error.message);
      } finally {
        setIsLoading(false);
      }
    };
    fetchComments();
  }, [event?.id]);

  // Handle form submission for new comment
  const onSubmit = async () => {
    if (!event?.id || !comment.trim()) return;
    try {
      setIsLoading(true);
      const newComment = await end_point.writeComment(comment, event.id);
      setComments(prev => [newComment, ...prev]);
      setComment(''); // Clear input field
    } catch (error) {
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle delete
  const handleDelete = async (commentId) => {
    try {
      setIsLoading(true);
      await end_point.deleteComment(commentId);
      setComments(prev => prev.filter(comment => comment.id !== commentId));
    } catch (error) {
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle edit
  const startEditing = (comment) => {
    setEditingId(comment.id);
    setEditContent(comment.content);
  };

  const saveEdit = async (commentId) => {
    try {
      setIsLoading(true);
      const updatedComment = await end_point.editComment(commentId, editContent);
      setComments(prev =>
        prev.map(comment => (comment.id === commentId ? updatedComment : comment))
      );
      setEditingId(null);
    } catch (error) {
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const cancelEditing = () => {
    setEditingId(null);
    setEditContent('');
  };

  // JSX rendering the component
  return (
    <div className="bg-white rounded-xl shadow-sm flex flex-col h-[600px]">
      <div className="p-6 border-b">
        <div className="flex items-center gap-2">
        <FiMessageSquare className="w-5 h-5 text-dark-purple" />
        <h2 className="text-2xl font-semibold text-dark-purple">Comments</h2>
        </div>
      </div>
      {error && <div className="text-red-500 mb-4">{error}</div>}

      <div className="flex-1 overflow-y-auto p-6">
      <div className="space-y-6">
      {comments.map((comment) => (
  <div key={comment.id} className="border-b pb-4 last:border-0 flex items-start space-x-4">
    <div className="avatar h-10 w-10">
      <img
        src={comment.user.profile_picture}
        alt={comment.user.name}
        className="rounded-full w-10 h-10"
      />
    </div>
    <div className="flex-1">
      {/* User info and date */}
      <div className="flex justify-between mb-1">
        <span className="font-medium text-gray-800">{comment.user.username}</span>
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-500">
            {new Date(comment.created_at).toLocaleDateString()}
          </span>
          {comment.user.id == userId && (
            <div className="dropdown dropdown-end">
              <label tabIndex={0} className="btn btn-ghost btn-circle">
                <HiOutlineDotsVertical className="w-5 h-5 text-gray-500" />
              </label>
              <ul
                tabIndex={0}
                className="dropdown-content menu p-2 shadow bg-white rounded-box w-32"
              >
                <li>
                  <button onClick={() => startEditing(comment)} className="flex items-center gap-2 text-gray-600">
                    <FiEdit2 className="w-4 h-4" /> Edit
                  </button>
                </li>
                <li>
                  <button onClick={() => handleDelete(comment.id)} className="flex items-center gap-2 text-red-600">
                    <LuTrash2 className="w-4 h-4" /> Delete
                  </button>
                </li>
              </ul>
            </div>
          )}
        </div>
      </div>
      
      {/* Comment content and edit input */}
      {editingId === comment.id ? (
        <div className="flex gap-2 mt-2">
          <input
            type="text"
            value={editContent}
            onChange={(e) => setEditContent(e.target.value)}
            className="flex-1 bg-white rounded-lg border border-gray-300 px-3 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
            autoFocus
          />
          <button
            onClick={() => saveEdit(comment.id)}
            disabled={!editContent.trim()}
            className={`p-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors ${
              !editContent.trim() ? 'opacity-50 cursor-not-allowed' : ''
            }`}
            title="Save"
          >
            <LuCheck className="w-4 h-4" />
          </button>
          <button
            onClick={cancelEditing}
            className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            title="Cancel"
          >
            <LuX className="w-4 h-4" />
          </button>
        </div>
      ) : (
        <p className="text-gray-600 mt-2">{comment.content}</p>
      )}
    </div>
  </div>
))}
 </div>

 </div>
    <div className="p-6 border-t">  
      <form onSubmit={handleSubmit(onSubmit)} className="flex gap-2">
        <input
          type="text"
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          placeholder="Add a comment..."
          className="flex-1 bg-white rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          className="bg-dark-purple text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
        >
          <LuSend className="w-4 h-4" />
          Send
        </button>
        </form>
      </div>
    </div>
  );
}
